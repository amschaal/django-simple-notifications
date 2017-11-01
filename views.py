from django.shortcuts import render, redirect
from models import Notification
from datetime import datetime
from notifications.utils import get_or_create_subscriptions
from django.template.context import RequestContext
from notifications.forms import NotificationSubscriptionFormset
from notifications import DELETE_NOTIFICATION
from django.contrib.auth.decorators import login_required

# @deprecated - use notifications middleware to process notification_id in url from notification.get_url()
@login_required
def redirect_to_url(request,pk):
    try:
        notification = Notification.objects.get(user=request.user,id=pk)
        url = notification.url
        if notification.type:
            if notification.is_aggregate:
                notifications = Notification.objects.filter(aggregate=notification)
                if DELETE_NOTIFICATION:
                    notifications.delete()
                else:
                    notifications.update(seen=datetime.now())
        if DELETE_NOTIFICATION:
            notification.delete()
        else:
            notification.seen = datetime.now()
            notification.save()
        return redirect(url)
    except:
        return redirect(request.META.get('HTTP_REFERER'))

@login_required
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
    return render(request, 'notifications/subscriptions.html', {'formset':formset})