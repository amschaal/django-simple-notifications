from rest_framework import serializers
from notifications.models import Notification, UserNotification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification

class UserNotificationSerializer(serializers.ModelSerializer):
    notification = NotificationSerializer(many=False)#serializers.RelatedField(many=False)
    class Meta:
        model = UserNotification
