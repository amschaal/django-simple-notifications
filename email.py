from django.utils import timezone
from django.conf import settings
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
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL ,[user.email], fail_silently=False,html_message=html_body)

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
