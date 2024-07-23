from rest_framework import generics
from .models import Orientation
from .serializers import OrientationSerializer
from .permissions import IsAdminOrReadOnly, IsAuthenticatedReadOnly

class OrientationList(generics.ListCreateAPIView):
    queryset = Orientation.objects.all()
    serializer_class = OrientationSerializer
   
    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminOrReadOnly]
        else:
            self.permission_classes = [IsAuthenticatedReadOnly]
        return super(OrientationList, self).get_permissions()

class OrientationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Orientation.objects.all()
    serializer_class = OrientationSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminOrReadOnly]
        else:
            self.permission_classes = [IsAuthenticatedReadOnly]
        return super(OrientationDetail, self).get_permissions()