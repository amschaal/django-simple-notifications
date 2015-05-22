from django.shortcuts import render, redirect
from models import Notification, UserNotification
from datetime import datetime

def redirect_to_url(request,pk):
    try:
        user_notification = UserNotification.objects.get(user=request.user,notification_id=pk)
        user_notification.seen = datetime.now()
        user_notification.save()
        return redirect(user_notification.notification.url)
    except:
        return redirect(request.META.get('HTTP_REFERER'))
    