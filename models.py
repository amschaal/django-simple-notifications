from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

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
    is_aggregate = models.BooleanField(default=False)
    aggregate = models.ForeignKey('self',null=True, related_name='notifications')
    user = models.ForeignKey(User)
    seen = models.DateTimeField(null=True,blank=True)
    url = models.URLField()
    text = models.CharField(max_length=250)
    description = models.TextField()
    created = models.DateTimeField(auto_now=True)
    importance = models.CharField(max_length=10,choices=((IMPORTANCE_LOW,'Low'),(IMPORTANCE_MEDIUM,'Medium'),(IMPORTANCE_HIGH,'High')))
    content_type = models.ForeignKey(ContentType,null=True)
    object_id = models.CharField(max_length=30,null=True) #Can be coerced into integer key if necessary
    content_object = GenericForeignKey('content_type', 'object_id')
    def short_datetime(self):
        return self.created.strftime('%b %d, %-I:%M%p')

# class UserNotification(models.Model):
# #     aggregate = models.BooleanField(default=False)
# #     aggregated_to = models.ForeignKey('UserNotification',null=True,blank=True)
#     notification = models.ForeignKey(Notification)
#     user = models.ForeignKey(User)
#     seen = models.DateTimeField(null=True,blank=True)

class NotificationSubscription(models.Model):
    user = models.ForeignKey(User,related_name='notification_subscriptions')
    type = models.ForeignKey(NotificationType,related_name='notification_subscriptions')
    subscribe = models.BooleanField(default=True)
    email = models.BooleanField(default=False)
    class Meta:
        unique_together = (("user", "type"),)

class UserSubscription(models.Model):
    user = models.ForeignKey(User,related_name='user_subscriptions')
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=30) #Can be coerced into integer key if necessary
    content_object = GenericForeignKey('content_type', 'object_id')
    subscribed = models.BooleanField(default=True)
    email = models.BooleanField(default=False)
    class Meta:
        unique_together = (("user", "content_type", "object_id"),)
    

