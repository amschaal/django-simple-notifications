from models import NotificationSubscription
import datetime
from django.utils import timezone
from django.utils.module_loading import import_string
from django.conf import settings
from utils import get_aggregated
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.models import User
from notifications.models import NotificationType, Notification
from django.db.models.query_utils import Q

EMAIL_FREQUENCY_HOURS = 24
if hasattr(settings,'NOTIFICATION_EMAIL_FREQUENCY_HOURS'):
    EMAIL_FREQUENCY_HOURS = settings.NOTIFICATION_EMAIL_FREQUENCY_HOURS

def email_user_notifications(user,notifications):
    context = {'user':user,'notifications':notifications, 'SITE_URL':settings.SITE_URL}
    body = render_to_string('notifications/notification_email_body.txt',context)
    html_body = render_to_string('notifications/notification_email_body.html',context)
    subject = render_to_string('notifications/notification_email_subject.txt',context)
    send_mail(subject, body, 'no-reply@genomecenter.ucdavis.edu',[user.email], fail_silently=False,html_message=html_body)
def email_notifications():
    # Returning all users, why?
    for u in User.objects.filter(notifications__aggregate__isnull=True,notifications__seen__isnull=True,notifications__emailed__isnull=True):
        types = NotificationType.objects.filter(notification_subscriptions__email=True,notification_subscriptions__user=u)
        notifications = Notification.objects.filter(aggregate__isnull=True,seen__isnull=True,emailed__isnull=True,user=u).filter(Q(type__in=types)|Q(type__isnull=True))
        print u
        print notifications
        if notifications.count() > 0:
            email_user_notifications(u, notifications)
            notifications.update(emailed=timezone.now())
# def email_notifications_old(after_datetime=timezone.now()-datetime.timedelta(hours=EMAIL_FREQUENCY_HOURS)):
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
#         if len(notifications) != 0:
#             email_user_notifications(user, notifications)