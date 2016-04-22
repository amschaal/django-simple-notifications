from django.utils.datetime_safe import datetime

from notifications import DELETE_NOTIFICATION
from notifications.models import Notification


class NotificationMiddleware(object):
    def process_request(self,request):
        notification_id = request.GET.get('notification_id',None)
        if notification_id and request.user:
            try:
                notification = Notification.objects.get(user=request.user,id=notification_id)
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
            except:
                pass
        return None