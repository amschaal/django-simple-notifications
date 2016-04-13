from models import Notification
# from utils import get_notifications
def notifications(request):
    if not request.user.is_authenticated():
        return {}
    notifications = Notification.objects.filter(user=request.user,seen__isnull=True,aggregate__isnull=True).order_by('-id')
    return {'notifications':notifications}