from django.urls import path
from .views import OrientationList, OrientationDetail

urlpatterns = [
    path('orientation/', OrientationList.as_view(), name='orientation-list'),
    path('orientation/<int:pk>/', OrientationDetail.as_view(), name='orientation-detail'),
]