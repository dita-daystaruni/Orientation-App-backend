from rest_framework import generics
from .models import Event
from .serializers import EventSerializer
from rest_framework.permissions import AllowAny

class ActivityList(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]

class ActivityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer