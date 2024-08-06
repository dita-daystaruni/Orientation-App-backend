from rest_framework import serializers
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'admission_number', 'course', 'phone_number', 'user_type', 'campus']

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
        

