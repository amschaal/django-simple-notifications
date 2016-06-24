from models import Notification, NotificationTypeSubscription
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
import operator
from django.utils.module_loading import import_string
from django.conf import settings
from notifications.models import NotificationType, UserSubscription
from notifications.signals import notification_created



"""
users - Should be a queryset of User objects
groups - Should be a queryset of Group objects for all groups whose users should be notified
instance - Model instance that users are subscribed to through UserSubscription
super_users - Set to True if super users should be notified
"""
def create_notification(url,text,type_id=None,importance=Notification.IMPORTANCE_LOW, description='',groups=None,users=None, instance=None,super_users=False, exclude_user=None):
    #Create queryset for notified users
    print users
    query_params = []
    if users:
        query_params.append(Q(id__in=users))
    if groups:
        query_params.append(Q(id__in=User.objects.filter(groups__in=groups)))
    if instance:
        ct = ContentType.objects.get_for_model(instance)
        query_params.append(Q(id__in=[subscription.user_id for subscription in UserSubscription.objects.filter(object_id=str(instance.id),content_type=ct,subscribed=True)]))
#         query_params.append(Q(user_subscriptions=UserSubscription.objects.filter(object_id=str(instance.id),content_type=ct,subscribed=True)))
    if super_users:
        query_params.append(Q(is_superuser=True))
    users = User.objects.filter(reduce(operator.or_, query_params))
    if exclude_user:
        users = users.exclude(id=exclude_user.id)

#     print groups
#     print instance
#     print super_users
#     print users
    if type_id:
        users = users.filter(notification_subscriptions__type_id=type_id,notification_subscriptions__subscribe=True)
        for s in NotificationTypeSubscription.objects.filter(user__in = users, type_id = type_id).select_related('user'):
#             UserNotification.objects.create(notification=notification,user=s.user)
            if instance:
                notification = Notification.objects.create(user=s.user,url=url,text=text,type_id=type_id,importance=importance,description=description,content_object=instance)
            else:
                notification = Notification.objects.create(user=s.user,url=url,text=text,type_id=type_id,importance=importance,description=description)
            notifications = Notification.objects.filter(user=s.user,url=url,type_id=type_id,seen__isnull=True,is_aggregate=False)
            print "NOTIFICATIONS"
            print notifications
            #Handle aggregate cases
            if notifications.count() > 1 and notification.type.aggregable:
                aggregated = get_aggregated(type_id,notifications)
                try:
                    aggregate = Notification.objects.get(user=s.user,url=url,type_id=type_id,is_aggregate=True,seen__isnull=True)
                    aggregate.text = aggregated['text']
                    aggregate.description = aggregated['description']
                    aggregate.emailed = None
                    aggregate.save()
                except Notification.DoesNotExist:
                    if instance:
                        aggregate = Notification.objects.create(user=s.user,url=url,type_id=type_id,is_aggregate=True,text=aggregated['text'],description=aggregated['description'],importance=importance,content_object=instance)
                    else:
                        aggregate = Notification.objects.create(user=s.user,url=url,type_id=type_id,is_aggregate=True,text=aggregated['text'],description=aggregated['description'],importance=importance)
                notifications.update(aggregate=aggregate)
            if s.email and s.user.email:
                # @todo: email, or maybe this should only be done every some number of minutes?
                pass
            #@todo: aggregate unseen UserNotifications that have the same type and URL from the past N minutes
    else:
        for u in users:
#             UserNotification.objects.create(notification=notification,user=u)
            notification = Notification.objects.create(user=s.user,url=url,text=text,importance=importance,description=description)
    notification_created.send(sender=Notification,url=url,text=text,type_id=type_id,importance=importance, description=description,groups=groups,users=users, instance=instance,super_users=super_users, exclude_user=exclude_user)

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


# Use this in post_save User model signal when users are created.  Otherwise, 
def get_or_create_subscriptions(user):
    types = NotificationType.objects.all()
    for type in types:
        configuration = get_notification_type_configuration(type.id)
        if configuration.user_can_subscribe(user):
            NotificationTypeSubscription.objects.get_or_create(user=user,type=type)
    return NotificationTypeSubscription.objects.filter(user=user)


