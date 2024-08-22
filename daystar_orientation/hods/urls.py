from django.urls import path
from .views import HODList, HODDetail

urlpatterns = [
    path('hods/', HODList.as_view(), name='hod-list'),
    path('hods/<int:pk>/', HODDetail.as_view(), name='hod-detail'),
]
