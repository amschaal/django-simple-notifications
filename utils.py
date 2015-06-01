from models import Notification, UserNotification, NotificationSubscription
from django.contrib.auth.models import User, Group
from django.db.models import Q
import operator
import datetime
from django.utils import timezone
from django.utils.module_loading import import_string
from django.conf import settings
from notifications.models import NotificationType




"""
users - Should be a queryset of User objects
groups - Should be a queryset of Group objects for all groups whose users should be notified
super_users - Set to True if super users should be notified
"""
def create_notification(url,text,type_id=None,importance=Notification.IMPORTANCE_LOW, description='',groups=None,users=None,super_users=False):
    if type_id:
        notification = Notification.objects.create(url=url,text=text,type_id=type_id,importance=importance,description=description)
    else:
        notification = Notification.objects.create(url=url,text=text,importance=importance,description=description)
    query_params = []
    if users:
        query_params.append(Q(id__in=users))
    if groups:
        query_params.append(Q(id__in=User.objects.filter(groups__in=groups)))
    if super_users:
        query_params.append(Q(is_superuser=True))
    users = User.objects.filter(reduce(operator.or_, query_params))
    # @todo: make UserNotifications more efficient with bulk create
    if type_id:
        users = users.filter(notification_subscriptions__type_id=type_id,notification_subscriptions__subscribe=True)
        for s in NotificationSubscription.objects.filter(user__in = users, type_id = type_id).select_related('user'):
            UserNotification.objects.create(notification=notification,user=s.user)
            if s.email and s.user.email:
                # @todo: email, or maybe this should only be done every some number of minutes?
                pass
            #@todo: aggregate unseen UserNotifications that have the same type and URL from the past N minutes
    else:
        for u in users:
            UserNotification.objects.create(notification=notification,user=u)


def get_notification_type_configuration(type_id):
    notification_type_dictionaries = getattr(settings,'NOTIFICATION_TYPES')
    for notification_type_dictionary in notification_type_dictionaries:
        notification_types = import_string(notification_type_dictionary)
        if notification_types.has_key(type_id):
            return notification_types[type_id]
    return {}

def get_aggregated(type_id,user_notifications):
    configuration = get_notification_type_configuration(type_id)
    aggregated={}
    aggregated['text'] = configuration.aggregated_text(user_notifications)
    aggregated['description'] = configuration.aggregated_description(user_notifications)
    return aggregated


"""
Couldn't think of a better way to aggregate notifications of the same type using Django ORM.
Query all unseen notifications and create curated list with "aggregated" notifications.
"""
def get_notifications(user,subscribed=True,email=False):
    print 'get notifications!!!!!!!!!'
    user_notifications = UserNotification.objects.filter(user=user,seen__isnull=True).select_related('notification','notification__type').order_by('-id')
    subscription_dict = {}
    for subscription in NotificationSubscription.objects.filter(user=user).select_related('type'):
        subscription_dict[subscription.type.id] = {'subscribe':subscription.subscribe,'email':subscription.email}
    
    #notification_by_type dictionary will hold number of times notifications with the same type and url occur (using type+url as dictionary key)
    notifications_by_type = {};
    notifications = []
    for un in user_notifications:
        if un.notification.type:
            #Skip some notifications based on subscriptions
            try:
                if subscribed and not subscription_dict[un.notification.type.id]['subscribe']:
                    continue
                if email and not subscription_dict[un.notification.type.id]['email']:
                    continue
            except:
                continue
        if not un.notification.type:
            notifications.append(un)
        elif not un.notification.type.aggregable:
            notifications.append(un)
        elif not notifications_by_type.has_key(un.notification.type.id+un.notification.url):
            notifications_by_type[un.notification.type.id+un.notification.url] = [un]
            notifications.append(un)
        elif notifications_by_type.has_key(un.notification.type.id+un.notification.url):
            notifications_by_type[un.notification.type.id+un.notification.url].append(un)
    for n in notifications:
        if n.notification.type:
            if notifications_by_type.has_key(n.notification.type.id+n.notification.url):
                if len(notifications_by_type[n.notification.type.id+n.notification.url]) > 1:
                    aggregated = get_aggregated(n.notification.type.id, notifications_by_type[n.notification.type.id+n.notification.url])
                    n.aggregated_text = aggregated['text']
                    n.aggregated_description = aggregated['description']
    print notifications_by_type
    return notifications

# Use this in post_save User model signal when users are created.  Otherwise, 
def get_or_create_subscriptions(user):
    types = NotificationType.objects.all()
    for type in types:
        configuration = get_notification_type_configuration(type.id)
        if configuration.user_can_subscribe(user):
            NotificationSubscription.objects.get_or_create(user=user,type=type)
    return NotificationSubscription.objects.filter(user=user)


# def email_notifications(after_datetime=timezone.now()-datetime.timedelta(hours=24)):
#     all_user_notifications = {}
#     for un in UserNotification.objects.filter(notification__created__gte=after_datetime,notification__type__isnull=False,seen__isnull=True).select_related('notification','user','notification__type').order_by('-id'):#prefetch_related('notification__type__notification_subscriptions').
#         if not all_user_notifications.has_key(str(un.user.id)):
#             all_user_notifications[str(un.user.id)] = {'user':un.user,'user_notifications':[],'notifications':[],'notification_by_type' : {},'subscription_dict':{}}
#         all_user_notifications[str(un.user.id)]['user_notifications'].append(un)
#     
#     
#     for subscription in NotificationSubscription.objects.filter(user_id__in=all_user_notifications.keys()).select_related('type','user'):
#         all_user_notifications[str(subscription.user.id)]['subscription_dict'][subscription.type.id]={'subscribe':subscription.subscribe,'email':subscription.email}
#     
#     print all_user_notifications
#     for user_dictionary in all_user_notifications.itervalues():
#         user = user_dictionary['user']
#         user_notifications = user_dictionary['user_notifications']
#         notifications = []#user_dictionary['notifications']
#         notifications_by_type = {}
#         if user_dictionary.has_key('notifications_by_type'):
#             notifications_by_type = user_dictionary['notifications_by_type']
#         subscription_dict = user_dictionary['subscription_dict']
#         for un in user_notifications:
#             if not subscription_dict[un.notification.type.id]['email']:
#                 continue
#             if not un.notification.type.aggregable:
#                 notifications.append(un)
#             elif not notifications_by_type.has_key(un.notification.type.id+un.notification.url):
#                 notifications_by_type[un.notification.type.id+un.notification.url] = [un]
#                 notifications.append(un)
#             elif notifications_by_type.has_key(un.notification.type.id+un.notification.url):
#                 notifications_by_type[un.notification.type.id+un.notification.url].append(un)
#         for n in notifications:
#             if notifications_by_type.has_key(n.notification.type.id+n.notification.url):
#                 if len(notifications_by_type[n.notification.type.id+n.notification.url]) > 1:
#                     aggregated = get_aggregated(n.notification.type.id, notifications_by_type[n.notification.type.id+n.notification.url])
#                     n.aggregated_text = aggregated['text']
#                     n.aggregated_description = aggregated['description']
# #         print notifications_by_type
#         print user
#         print notifications
    