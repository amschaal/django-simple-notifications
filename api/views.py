from rest_framework import viewsets, status
from notifications.api.serializers import UserSubscriptionSerializer,\
    NotificationSerializer
from notifications.models import UserSubscription,\
    Notification
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.decorators import detail_route

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    filter_backends = (filters.DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter,)
    model = Notification
    search_fields = ('text', 'description','importance','seen')
    filter_fields = ('importance','seen','aggregate','id','type','content_type','object_id')
    ordering_fields = ('text', 'description','importance','seen','created')
    def get_queryset(self):
        queryset = Notification.objects.filter(user=self.request.user,aggregate__isnull=True).order_by('-id')
        if 'new' in self.request.query_params:
            new = self.request.query_params['new']
            print new
            if new in ['True','true','1']:
                print 'True!!!'
                queryset = queryset.filter(seen__isnull=True)
            elif new in ['False','false','0']:
                print 'False!!!'
                queryset = queryset.filter(seen__isnull=False)
        return queryset

class UserSubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = UserSubscriptionSerializer
#     permission_classes = [CustomPermission]
    filter_fields = ('content_type', 'object_id', 'content_type__model')
    model = UserSubscription
    def get_queryset(self):
        return UserSubscription.objects.filter(user=self.request.user)
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    @detail_route(methods=['delete'])
    def clear(self, request, pk=None):
        instance = self.get_object()
        Notification.objects.filter(content_type=instance.content_type,object_id=instance.object_id).delete()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
#     def get_queryset(self):
#         return Note.objects.all()#get_all_user_objects(self.request.user, ['view'], Experiment)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
#     def perform_update(self, serializer):
#         serializer.save(user=self.request.user)