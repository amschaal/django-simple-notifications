from models import Notification, UserNotification
def notifications(request):
    if not request.user.is_authenticated():
        return {}
    user_notifications = UserNotification.objects.filter(user=request.user).select_related('notification')
    return {'user_notifications':user_notifications}