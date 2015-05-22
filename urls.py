from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^notifications/(?P<pk>\d+)/$', 'notifications.views.redirect_to_url', name='notifications_redirect_to_url'),
)

