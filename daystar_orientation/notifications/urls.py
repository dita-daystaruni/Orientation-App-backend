from django.urls import path
from .views import NotificationList, NotificationDetail, RecentNotificationList, RegisterDevice

urlpatterns = [
    path('notifications/', NotificationList.as_view(), name='notification-list'),
    path('notifications/<int:pk>/', NotificationDetail.as_view(), name='notification-detail'),
    path('recent/', RecentNotificationList.as_view(), name='recent-notifications'),
    path('register-device/', RegisterDevice.as_view(), name='register_device'),
]