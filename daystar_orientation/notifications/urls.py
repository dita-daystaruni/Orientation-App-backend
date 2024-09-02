from django.urls import path
from .views import NotificationList, NotificationDetail, RecentNotificationList, RegisterDevice, notifications_view, notificationedit_view,notificationadd_view

urlpatterns = [
    path('notifications/', NotificationList.as_view(), name='notification-list'),
    path('notifications/<int:pk>/', NotificationDetail.as_view(), name='notification-detail'),
    path('recent/', RecentNotificationList.as_view(), name='recent-notifications'),
    path('notifications_view/', notifications_view, name='notifications'),
    path('notifications_view/edit/', notificationedit_view, name='notifications_edit'),
    path('notifications_view/add/', notificationadd_view, name='notifications_add'),
    path('register-device/', RegisterDevice.as_view(), name='register_device'),
]