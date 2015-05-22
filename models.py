from django.db import models
from django.contrib.auth.models import User

class NotificationType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True,null=True)

class Notification(models.Model):
    IMPORTANCE_LOW = 'low'
    IMPORTANCE_MEDIUM = 'medium'
    IMPORTANCE_HIGH = 'high'
    type = models.ForeignKey(NotificationType, blank=True, null=True)
    url = models.URLField()
    text = models.CharField(max_length=250)
    description = models.TextField()
    created = models.DateTimeField(auto_now=True)
    importance = models.CharField(max_length='10',choices=((IMPORTANCE_LOW,'Low'),(IMPORTANCE_MEDIUM,'Medium'),(IMPORTANCE_HIGH,'High')))

class UserNotification(models.Model):
    notification = models.ForeignKey(Notification)
    user = models.ForeignKey(User)
    seen = models.DateTimeField(null=True,blank=True)

class NotificationSubscription(models.Model):
    user = models.ForeignKey(User,related_name='notification_subscriptions')
    type = models.ForeignKey(NotificationType)
    email = models.BooleanField(default=False)
