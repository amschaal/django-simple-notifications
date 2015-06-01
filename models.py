from django.db import models
from django.contrib.auth.models import User
from datetime import date

class NotificationType(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True,null=True)
    aggregable = models.BooleanField(default=False)
    aggregated_text = models.CharField(max_length=250,blank=True,null=True) #Use %d in text to be replaced by the number of notifications aggregated

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
    def short_datetime(self):
        return self.created.strftime('%b %d, %-I:%M%p')

class UserNotification(models.Model):
#     aggregate = models.BooleanField(default=False)
#     aggregated_to = models.ForeignKey('UserNotification',null=True,blank=True)
    notification = models.ForeignKey(Notification)
    user = models.ForeignKey(User)
    seen = models.DateTimeField(null=True,blank=True)

class NotificationSubscription(models.Model):
    user = models.ForeignKey(User,related_name='notification_subscriptions')
    type = models.ForeignKey(NotificationType,related_name='notification_subscriptions')
    subscribe = models.BooleanField(default=True)
    email = models.BooleanField(default=False)
    class Meta:
        unique_together = (("user", "type"),)
    

