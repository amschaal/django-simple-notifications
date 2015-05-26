from django.shortcuts import render, redirect
from models import Notification, UserNotification
from datetime import datetime

def redirect_to_url(request,pk):
    try:
        user_notification = UserNotification.objects.get(user=request.user,notification_id=pk)
        if user_notification.notification.type:
            if user_notification.notification.type.aggregable:
                UserNotification.objects.filter(user=request.user,notification__url=user_notification.notification.url,notification__type__id=user_notification.notification.type.id).update(seen=datetime.now())
                return redirect(user_notification.notification.url)
        user_notification.seen = datetime.now()
        user_notification.save()
        return redirect(user_notification.notification.url)
    except:
        return redirect(request.META.get('HTTP_REFERER'))
    