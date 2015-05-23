from models import Notification, UserNotification
def notifications(request):
    if not request.user.is_authenticated():
        return {}
    user_notifications = UserNotification.objects.filter(user=request.user,seen__isnull=True).select_related('notification').order_by('-id')
    return {'user_notifications':user_notifications}