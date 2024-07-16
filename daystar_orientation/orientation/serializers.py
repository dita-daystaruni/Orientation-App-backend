from rest_framework import serializers
from .models import Orientation

class OrientationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orientation
        fields = '__all__'
