from rest_framework import generics
from .models import HOD, Course
from .serializers import HODSearializer, CourseSerializer
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
    

class CourseList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminOrReadOnly]
        else:
            self.permission_classes = [IsAuthenticatedReadOnly]
        return super().get_permissions()

class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all() 
    serializer_class = CourseSerializer
    lookup_field = 'name'

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminOrReadOnly]
        else:
            self.permission_classes = [IsAuthenticatedReadOnly]
        return super().get_permissions()