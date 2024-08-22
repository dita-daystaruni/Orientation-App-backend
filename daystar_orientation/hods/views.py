from rest_framework import generics
from .models import HOD
from .serializers import HODSearializer
from .permissions import IsAdminOrReadOnly, IsAuthenticatedReadOnly

class HODList(generics.ListCreateAPIView):
    queryset = HOD.objects.all()
    serializer_class = HODSearializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminOrReadOnly]
        else:
            self.permission_classes = [IsAuthenticatedReadOnly]
        return super(HODList, self).get_permissions()

class HODDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = HOD.objects.all()
    serializer_class = HODSearializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminOrReadOnly]
        else:
            self.permission_classes = [IsAuthenticatedReadOnly]
        return super(HODDetail, self).get_permissions()