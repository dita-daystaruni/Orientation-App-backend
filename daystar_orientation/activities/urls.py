from django.urls import path
from . import views

urlpatterns = [
    path('activities/', views.ActivityList.as_view()),
    path('activities/<int:pk>/', views.ActivityDetail.as_view()),
]