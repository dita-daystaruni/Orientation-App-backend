from rest_framework import serializers
from .models import HOD

class HODSearializer(serializers.ModelSerializer):
    class Meta:
        model = HOD
        fields = '__all__'

class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HOD
        fields = ['first_name', 'last_name', 'email', 'phone_number']