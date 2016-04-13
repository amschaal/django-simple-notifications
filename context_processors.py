from models import Notification
# from utils import get_notifications
def notifications(request):
    if not request.user.is_authenticated():
        return {}
    user_notifications = Notification.objects.filter(user=request.user,seen__isnull=True,aggregate__isnull=True).order_by('-id')
    
#     user_notifications = get_notifications(user=request.user)
    return {'user_notifications':user_notifications}