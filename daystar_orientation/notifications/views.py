from rest_framework import generics
from .models import Notification
from .serializers import NotificationSerializer
from .permissions import IsAdminOrReadOnly, IsAuthenticatedReadOnly
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseForbidden

class NotificationList(generics.ListCreateAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user = self.request.user

        if user.user_type == 'admin':
            return Notification.objects.filter(is_admin_viewer=True)
        elif user.user_type == 'parent':
            return Notification.objects.filter(
                Q(created_by=user) | 
                Q(is_regular_viewer=True) & Q(created_by__parent=user)
            )
        elif user.user_type == 'regular':
            return Notification.objects.filter(
                is_regular_viewer=True,
                created_by__parent=user  
            )
        return Notification.objects.none() 

    def perform_create(self, serializer):
        user = self.request.user
        notification = serializer.save(created_by=user)

        if user.user_type == 'admin':
            admin_viewers = self.request.data.get('is_admin_viewer', False)
            parent_viewers = self.request.data.get('is_parent_viewer', False)
            regular_viewers = self.request.data.get('is_regular_viewer', False)

            notification.is_admin_viewer = admin_viewers
            notification.is_parent_viewer = parent_viewers
            notification.is_regular_viewer = regular_viewers

        elif user.user_type == 'parent':
            notification.is_regular_viewer = True 
            notification.is_parent_viewer = True  

        notification.save()


class NotificationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminOrReadOnly]
        else:
            self.permission_classes = [IsAuthenticatedReadOnly]
        return super().get_permissions()
    
class RecentNotificationList(generics.ListAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.order_by('-created_at')[:3]
    
# Web views.
@login_required
def notifications_view(request):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("You are not authorized to view this page.")
    
    notifications = Notification.objects.all()
    return render(request, 'notifications.html', {'notifications': notifications})

@login_required
def notificationadd_view(request):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("You are not authorized to view this page.")
    
    return render(request, 'notifications_add.html')

@login_required
def notificationedit_view(request):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("You are not authorized to view this page.")
    
    return render(request, 'notifications_edit.html')
