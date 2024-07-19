from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.ActivityList.as_view()),
    path('events/<int:pk>/', views.ActivityDetail.as_view()),
]