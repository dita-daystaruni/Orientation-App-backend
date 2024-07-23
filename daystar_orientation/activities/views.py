# activities/views.py

from rest_framework import generics
from .models import Activity
from .serializers import ActivitySerializer
from .permissions import IsAdminOrReadOnly, IsAuthenticatedReadOnly

class ActivityList(generics.ListCreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminOrReadOnly]
        else:
            self.permission_classes = [IsAuthenticatedReadOnly]
        return super(ActivityList, self).get_permissions()

class ActivityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminOrReadOnly]
        else:
            self.permission_classes = [IsAuthenticatedReadOnly]
        return super(ActivityDetail, self).get_permissions()
