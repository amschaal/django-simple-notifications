from django.shortcuts import render, redirect
from models import Notification, UserNotification, NotificationType
from datetime import datetime
from notifications.utils import get_notification_type_configuration, get_or_create_subscriptions
from django.template.context import RequestContext
from notifications.forms import NotificationSubscriptionFormset

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

def manage_subscriptions(request):
#     types = NotificationType.objects.all()
#     type_list = []
#     for type in types:
#         configuration = get_notification_type_configuration(type.id)
#         if configuration.user_can_subscribe(request.user):
#             type_list.append(type)
    subscriptions = get_or_create_subscriptions(request.user)
    if request.method == 'POST':
        formset = NotificationSubscriptionFormset(request.POST,queryset=subscriptions)
        formset.save()
    else:
        formset = NotificationSubscriptionFormset(queryset=subscriptions)
    return render(request, 'notifications/subscriptions.html', {'formset':formset},context_instance=RequestContext(request))