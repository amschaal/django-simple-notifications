from django.conf.urls import patterns, include, url

from rest_framework import routers
from notifications.api.views import NotificationViewSet, UserSubscriptionViewSet

router = routers.DefaultRouter()
router.register(r'notifications', NotificationViewSet,'Notification')
router.register(r'subscriptions', UserSubscriptionViewSet,'Subscriptions')

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/$', 'notifications.views.redirect_to_url', name='notifications_redirect_to_url'),
    url(r'^subscriptions/$', 'notifications.views.manage_subscriptions', name='notifications_manage_subscriptions'),
    url(r'^api/', include(router.urls)),
)

