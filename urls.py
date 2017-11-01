from django.conf.urls import include, url
from rest_framework import routers
from notifications.api.views import NotificationViewSet, UserSubscriptionViewSet
import views

router = routers.DefaultRouter()
router.register(r'notifications', NotificationViewSet,'Notification')
router.register(r'subscriptions', UserSubscriptionViewSet,'Subscriptions')

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', views.redirect_to_url, name='notifications_redirect_to_url'),
    url(r'^subscriptions/$', views.manage_subscriptions, name='notifications_manage_subscriptions'),
    url(r'^api/', include(router.urls)),
]

