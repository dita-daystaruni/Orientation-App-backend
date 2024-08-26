from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.first_name')
    
    class Meta:
        model = Notification
        fields = ['id', 'title', 'description', 'created_by', 'is_admin_viewer', 'is_parent_viewer', 'is_regular_viewer',  'created_at']
        read_only_fields = ['id', 'created_by', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user

        notification = Notification.objects.create(**validated_data)
        return notification
