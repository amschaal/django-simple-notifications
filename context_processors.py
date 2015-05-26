from models import Notification, UserNotification
from utils import get_notifications
def notifications(request):
    if not request.user.is_authenticated():
        return {}
#     user_notifications = UserNotification.objects.filter(user=request.user,seen__isnull=True).select_related('notification').order_by('-id')
    user_notifications = get_notifications(user=request.user)
    return {'user_notifications':user_notifications}