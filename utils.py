from models import Notification, UserNotification, NotificationSubscription
from django.contrib.auth.models import User, Group
from django.db.models import Q
import operator

"""
users - Should be a queryset of User objects
groups - Should be a queryset of Group objects for all groups whose users should be notified
super_users - Set to True if super users should be notified
"""
def create_notification(url,text,type=None,importance=Notification.IMPORTANCE_LOW, description='',groups=None,users=None,super_users=False):
    notification = Notification.objects.create(url=url,text=text,type=type,importance=importance,description='description')
    query_params = []
    if users:
        query_params.append(Q(id__in=users))
    if groups:
        query_params.append(Q(id__in=User.objects.filter(groups__in=groups)))
    if super_users:
        query_params.append(Q(is_superuser=True))
    users = User.objects.filter(reduce(operator.or_, query_params))
    # @todo: make UserNotifications more efficient with bulk create
    if type:
        for s in NotificationSubscription.objects.filter(user__in = users, type = type).select_related('user'):
            UserNotification.objects.create(notification=notification,user=s.user)
            if s.email and s.user.email:
                # @todo: email
                pass
    else:
        for u in users:
            UserNotification.objects.create(notification=notification,user=u)
        