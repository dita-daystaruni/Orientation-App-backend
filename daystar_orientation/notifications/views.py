from rest_framework import generics
from account.models import Account
from .models import Notification
from .serializers import NotificationSerializer
from .permissions import IsAdminOrReadOnly, IsAuthenticatedReadOnly
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message
from firebase_admin.messaging import Notification as Nots
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from django.contrib import messages

class NotificationList(generics.ListCreateAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user = self.request.user

        if user.user_type == 'admin':
            return Notification.objects.filter(is_admin_viewer=True)
        elif user.user_type == 'parent':
            return Notification.objects.filter(is_parent_viewer=True)
            # return Notification.objects.filter(
            #     Q(created_by=user) | 
            #     Q(is_regular_viewer=True) & Q(created_by__parent=user)
            # )
        elif user.user_type == 'regular':
            return Notification.objects.filter(
                is_regular_viewer=True,
                created_by__user_type="admin"
            ) | Notification.objects.filter(
                is_regular_viewer=True,
                created_by=user.parent
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
            self.send_push_notification(notification, user)

        elif user.user_type == 'parent':
            notification.is_regular_viewer = True 
            # notification.is_parent_viewer = True
            self.send_push_notification(notification, user)

        notification.save()

    def send_push_notification(self, notification, user):
        # Fetch intended users based on the notification's viewer settings
        users_to_notify = Account.objects.none()
        # notification is sent by an admin
        if user.user_type == "admin":
            if notification.is_admin_viewer:
                users_to_notify = users_to_notify | Account.objects.filter(user_type='admin')
            if notification.is_parent_viewer:
                users_to_notify = users_to_notify | Account.objects.filter(user_type='parent')
            if notification.is_regular_viewer:
                users_to_notify = users_to_notify | Account.objects.filter(user_type='regular')
        # notification is sent by a parent, send only to kids
        else:
            users_to_notify = users_to_notify | Account.objects.filter(user_type='regular', parent=user)

        # Fetch devices for the intended users
        devices = FCMDevice.objects.filter(user__in=users_to_notify)

        # Extract tokens from the devices
        tokens = [device.registration_id for device in devices if device.registration_id]

        # If there are no tokens, we shouldn't proceed
        if not tokens:
            # print("No tokens found for push notifications.")
            return

        # Create the message payload
        message = Message(
            notification=Nots(
                title=notification.title,
                body=notification.description,
            ),
            
        )

        # Send message to multiple device tokens
        try:
            # print(tokens)
            devices = FCMDevice.objects.filter(registration_id__in=tokens)
            output = devices.send_message(
                message,
            )
            
            # print(output.response.__dict__)

            # print(f"Push notification sent successfully to {len(tokens)} devices.")
            
        except Exception as e:
            raise e

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
        user = self.request.user

        if user.user_type == 'admin':
            notifications = Notification.objects.filter(is_admin_viewer=True)
            notifications = notifications.order_by('-created_at')[:3]
            return notifications
        elif user.user_type == 'parent':
            notifications = Notification.objects.filter(is_parent_viewer=True)
            notifications = notifications.order_by('-created_at')[:3]
            return notifications
        elif user.user_type == 'regular':
            notifications = Notification.objects.filter(
                is_regular_viewer=True,
                created_by__user_type="admin"
            ) | Notification.objects.filter(
                is_regular_viewer=True,
                created_by=user.parent
            )
            notifications = notifications.order_by('-created_at')[:3]
            return notifications
        return Notification.objects.none()

class RegisterDevice(APIView):
    def post(self, request):
        user = request.user
        registration_id = request.data.get('registration_id')
        
        if not registration_id:
            return Response({'error': 'Registration ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        device, created = FCMDevice.objects.get_or_create(
            user=user,
            registration_id=registration_id,
            defaults={'type': 'android'}
        )
        
        if created:
            return Response({'message': 'Device registered successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Device already registered'}, status=status.HTTP_200_OK)
    
# Web views.
@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(is_admin_viewer=True).order_by('-created_at')
    
    paginator = Paginator(notifications, 7) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'notifications.html', {'page_obj': page_obj})

@login_required
def notificationadd_view(request):
    if request.method == 'POST':
        title = request.POST.get('notificationTitle')
        description = request.POST.get('notificationDescription')
        is_admin_viewer = 'admins' in request.POST
        is_parent_viewer = 'instructors' in request.POST
        is_regular_viewer = 'students' in request.POST

        try:
            Notification.objects.create(
                title=title,
                description=description,
                created_by=request.user,
                is_admin_viewer=is_admin_viewer,
                is_parent_viewer=is_parent_viewer,
                is_regular_viewer=is_regular_viewer
            )
            messages.success(request, 'Notification created successfully.')
            return redirect('notifications')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, 'notifications_add.html')

    return render(request, 'notifications_add.html')
