from rest_framework import generics
from .models import Notification
from .serializers import NotificationSerializer
from .permissions import IsAdminOrReadOnly, IsAuthenticatedReadOnly
from account.models import Account

class NotificationList(generics.ListCreateAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(viewers=user)

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminOrReadOnly]
        else:
            self.permission_classes = [IsAuthenticatedReadOnly]
        return super().get_permissions()

    def perform_create(self, serializer):
        user = self.request.user
        
        notification = serializer.save(created_by=user)

        if user.user_type == 'admin':
            viewers = Account.objects.filter(user_type__in=['admin', 'parent', 'regular'])
            notification.viewers.set(viewers)
        elif user.user_type == 'parent':
            viewers = Account.objects.filter(user_type='regular')
            notification.viewers.set(viewers)


class NotificationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminOrReadOnly]
        else:
            self.permission_classes = [IsAuthenticatedReadOnly]
        return super().get_permissions()
    
class RecentNotificationList(generics.ListAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.order_by('-created_at')[:3]