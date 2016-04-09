from rest_framework import serializers
from notifications.models import Notification, UserNotification,\
    UserSubscription

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification

class UserNotificationSerializer(serializers.ModelSerializer):
    notification = NotificationSerializer(many=False)#serializers.RelatedField(many=False)
    class Meta:
        model = UserNotification

class UserSubscriptionSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField(many=False,read_only=True,required=False)
    class Meta:
        model = UserSubscription