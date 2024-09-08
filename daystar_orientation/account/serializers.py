from rest_framework import serializers
from .models import Account, Documents
import mimetypes
from hods.models import Course

class AccountSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Account
        fields = [
            'id', 'first_name', 'last_name', 'username', 'email', 'admission_number', 
            'course', 'phone_number', 'user_type', 'campus', 'gender', 
            'accomodation', 'checked_in', 'parent', 'password'
        ]
        read_only_fields = ['password']

    def create(self, validated_data):
        user = Account.objects.create_user(**validated_data)
        return user
    
    def to_representation(self, instance):
        """
        Appends request host on the images urls        
        """
        representation = super().to_representation(instance)
        if representation['email'] is None:
            representation['email'] = ''
        if representation['phone_number'] == "00000000000":
            representation['phone_number'] = ''
        return representation

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'user_type']
        read_only_fields = ['id', 'user_type']

class PasswordChangeSerializer(serializers.Serializer):
    admission_number = serializers.CharField()
    new_password = serializers.CharField(min_length=8, max_length=100)

class DocumentSerializer(serializers.ModelSerializer):

    def validate_file(self, value):
        mime_type, encoding = mimetypes.guess_type(value.name)

        valid_mime_types = [
            'application/pdf', 
            'image/jpeg',       
            'image/png',        
            'image/gif',        
            'image/bmp',     
        ]
        
        if mime_type not in valid_mime_types:
            raise serializers.ValidationError('Unsupported file type.')
        
        return value

    class Meta:
        model = Documents
        fields = ['id', 'user', 'title', 'file', 'uploaded_at', 'description']
        read_only_fields = ['id', 'uploaded_at', 'user']
