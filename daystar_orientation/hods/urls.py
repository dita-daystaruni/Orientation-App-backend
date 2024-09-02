from django.urls import path
from .views import HODList, HODDetail, CourseList, CourseDetail, hodsdetails_view, hodsadd_view, hodsedit_view, stats_view

urlpatterns = [
    path('hods/', HODList.as_view(), name='hod-list'),
    path('hods/<int:pk>/', HODDetail.as_view(), name='hod-detail'),
    path('courses/', CourseList.as_view(), name='course-list'),
    path('courses/<str:name>/', CourseDetail.as_view(), name='course-detail'),
    path('course-detail/', hodsdetails_view, name='courses_details'),
    path('course-detail/add/', hodsadd_view, name='courses_details_add'),
    path('course-detail/<int:pk>/edit/', hodsedit_view, name='courses_details_edit'),
    path('course-detail/<int:pk>/delete/', stats_view, name='courses_details_delete'),
    path('course-detail/stats/', stats_view, name='courses_stats'),
]
