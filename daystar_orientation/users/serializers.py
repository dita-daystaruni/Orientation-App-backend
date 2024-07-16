from rest_framework import serializers
from .models import User
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'admission_number', 'course', 'phone_number', 'email']

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'email', 'password', 'admission_number', 'course', 'phone_number']
