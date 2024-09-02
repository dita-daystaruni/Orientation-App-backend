from django.urls import path
from .views import ActivityList, ActivityDetail, activities_view, activitiesadd_view, activitiesedit_view

urlpatterns = [
    path('activities/', ActivityList.as_view(), name='activity-list'),
    path('activities/<int:pk>/', ActivityDetail.as_view(), name='activity-detail'),
    path('activities_view/', activities_view, name='activities'),
    path('activities_view/add/', activitiesadd_view, name='activities_add'),
    path('activities_view/edit/', activitiesedit_view, name='activities_edit'),
]