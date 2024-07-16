from rest_framework import generics
from .models import Orientation
from .serializers import OrientationSerializer

class OrientationList(generics.ListCreateAPIView):
    queryset = Orientation.objects.all()
    serializer_class = OrientationSerializer

class OrientationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Orientation.objects.all()
    serializer_class = OrientationSerializer