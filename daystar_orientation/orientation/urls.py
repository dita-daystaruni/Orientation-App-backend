from django.urls import path
from . import views

urlpatterns = [
    path('orientation/', views.OrientationList.as_view()),
    path('orientation/<int:pk>/', views.OrientationDetail.as_view()),
]