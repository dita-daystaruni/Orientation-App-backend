from rest_framework import generics
from .models import Orientation
from .serializers import OrientationSerializer
from rest_framework.permissions import AllowAny

class OrientationList(generics.ListCreateAPIView):
    queryset = Orientation.objects.all()
    serializer_class = OrientationSerializer
    permission_classes = [AllowAny]

class OrientationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Orientation.objects.all()
    serializer_class = OrientationSerializer