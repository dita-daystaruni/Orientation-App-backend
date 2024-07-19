from rest_framework import generics
from .models import FAQ
from .serializers import FAQSerializer
from rest_framework.permissions import AllowAny

class FAQList(generics.ListCreateAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [AllowAny]

class FAQDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer