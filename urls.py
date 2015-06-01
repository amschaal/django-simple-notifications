from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/$', 'notifications.views.redirect_to_url', name='notifications_redirect_to_url'),
    url(r'^subscriptions/$', 'notifications.views.manage_subscriptions', name='notifications_manage_subscriptions'),
)

