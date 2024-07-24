from rest_framework import serializers
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['username', 'admission_number', 'course', 'phone_number', 'email', 'email_verified', 'user_type']


