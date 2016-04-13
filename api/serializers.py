from rest_framework import serializers
from notifications.models import Notification, UserSubscription

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification

# class UserNotificationSerializer(serializers.ModelSerializer):
#     notification = NotificationSerializer(many=False)#serializers.RelatedField(many=False)
#     class Meta:
#         model = UserNotification

class UserSubscriptionSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField(many=False,read_only=True,required=False)
    notifications = serializers.SerializerMethodField()
    def get_notifications(self,obj):
        notifications = Notification.objects.filter(user=obj.user,content_type=obj.content_type,object_id=obj.object_id,aggregate__isnull=True,seen__isnull=True)
        return NotificationSerializer(notifications,many=True).data
    class Meta:
        model = UserSubscription