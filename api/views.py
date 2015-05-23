from rest_framework import viewsets
from notifications.api.serializers import  UserNotificationSerializer
from notifications.models import UserNotification
from rest_framework import filters

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserNotificationSerializer
    filter_backends = (filters.DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter,)
    model = UserNotification
    search_fields = ('notification__text', 'notification__description','notification__importance','seen')
    filter_fields = ('notification__text', 'notification__description','notification__importance','seen')
    ordering_fields = ('notification__text', 'notification__description','notification__importance','seen','notification__created')
    def get_queryset(self):
        queryset = UserNotification.objects.filter(user=self.request.user).select_related('notification').order_by('-id')
        if 'new' in self.request.QUERY_PARAMS:
            new = self.request.QUERY_PARAMS['new']
            print new
            if new in ['True','true','1']:
                print 'True!!!'
                queryset = queryset.filter(seen__isnull=True)
            elif new in ['False','false','0']:
                print 'False!!!'
                queryset = queryset.filter(seen__isnull=False)
        return queryset