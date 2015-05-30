from models import Notification, UserNotification, NotificationSubscription
from django.contrib.auth.models import User, Group
from django.db.models import Q
import operator

from django.utils.module_loading import import_string
from django.conf import settings




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
    if False:#type_id:
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
def get_notifications(user):
    print 'get notifications!!!!!!!!!'
    user_notifications = UserNotification.objects.filter(user=user,seen__isnull=True).select_related('notification','notification__type').order_by('-id')
#     type_counts = UserNotification.objects.filter(user=user,seen__isnull=True).values('id','notification__type')\
#     .annotate(num_values=Count('type'))

    #notification_by_type dictionary will hold number of times notifications with the same type and url occur (using type+url as dictionary key)
    notification_by_type = {};
    notifications = []
    for un in user_notifications:
        if not un.notification.type:
            
            print 1
            print un.notification.type
            notifications.append(un)
        elif not un.notification.type.aggregable:
            print 2
            notifications.append(un)
        elif not notification_by_type.has_key(un.notification.type.id+un.notification.url):
            print 3
            notification_by_type[un.notification.type.id+un.notification.url] = [un]
            notifications.append(un)
        elif notification_by_type.has_key(un.notification.type.id+un.notification.url):
            print 4
            notification_by_type[un.notification.type.id+un.notification.url].append(un)
    for n in notifications:
        if n.notification.type:
            if notification_by_type.has_key(n.notification.type.id+n.notification.url):
                if len(notification_by_type[n.notification.type.id+n.notification.url]) > 1:
                    aggregated = get_aggregated(n.notification.type.id, notification_by_type[n.notification.type.id+n.notification.url])
                    n.aggregated_text = aggregated['text']
                    n.aggregated_description = aggregated['description']
    print notification_by_type
    return notifications