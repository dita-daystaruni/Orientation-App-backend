from django.urls import path
from . import views

urlpatterns = [
    path('orientation/', views.OrientationList.as_view(), name='orientation-list'),
    path('orientation/<int:pk>/', views.OrientationDetail.as_view(), name='orientation-detail'),
]