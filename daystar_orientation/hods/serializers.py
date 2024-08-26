from rest_framework import serializers
from .models import HOD, Course

class HODSearializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())    

    class Meta:
        model = HOD
        fields = ['id', 'title', 'first_name', 'last_name', 'email', 'phone_number', 'course']
        read_only_fields = ['id','title']

class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HOD
        fields = ['id', 'title', 'first_name', 'last_name', 'email', 'phone_number', 'course']
        read_only_fields = ['id','title']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name']