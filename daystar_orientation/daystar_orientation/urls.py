# myproject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('orientation.urls')),
    path('api/', include('account.urls')),
    path('api/', include('faqs.urls')),
    path('api/', include('activities.urls')),
    path('api/', include('events.urls')),
]
