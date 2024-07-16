# myproject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('orientation.urls')),
    path('api/', include('users.urls')),
    path('api/', include('faqs.urls')),
    path('api/', include('activities.urls')),
]
