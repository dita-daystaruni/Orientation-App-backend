from rest_framework import generics
from .models import Notification
from .serializers import NotificationSerializer
from .permissions import IsAdminOrReadOnly, IsAuthenticatedReadOnly

class NotificationList(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
   
    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminOrReadOnly]
        else:
            self.permission_classes = [IsAuthenticatedReadOnly]
        return super(NotificationList, self).get_permissions()

class NotificationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminOrReadOnly]
        else:
            self.permission_classes = [IsAuthenticatedReadOnly]
        return super(NotificationDetail, self).get_permissions()