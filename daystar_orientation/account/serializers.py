from rest_framework import serializers
from .models import Account, Documents


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'admission_number', 'course', 'phone_number', 'user_type', 'campus', 'gender', 'accomodation', 'checked_in', 'parent', 'password']
        read_only_fields = ['password']

    def create(self, validated_data):
        user = Account.objects.create_user(**validated_data)
        return user

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone_number']

class PasswordChangeSerializer(serializers.Serializer):
    admission_number = serializers.CharField()
    new_password = serializers.CharField(min_length=8, max_length=100)

    def validate_new_password(self, value):
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        return value

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = ['id', 'user', 'title', 'file', 'uploaded_at', 'description']
        read_only_fields = ['id', 'uploaded_at', 'user']