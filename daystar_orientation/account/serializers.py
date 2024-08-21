from rest_framework import serializers
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'email', 'admission_number', 'course', 'phone_number', 'user_type', 'campus', 'gender', 'accomodation', 'checked_in', 'parent']

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
        

class ChildDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'first_name', 'last_name', 'admission_number', 'phone_number', 'campus']

class ParentSerializer(serializers.ModelSerializer):
    children = ChildDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'first_name', 'last_name', 'admission_number', 'campus', 'phone_number', 'children']

class ChildSerializer(serializers.ModelSerializer):
    parent_details = ParentSerializer(source='parent', read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'first_name', 'last_name', 'admission_number', 'campus', 'phone_number', 'parent_details']
