from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('orientation/', include('orientation.urls')),
    path('account/', include('account.urls')),
    path('faqs/', include('faqs.urls')),
    path('activities/', include('activities.urls')),
    path('events/', include('events.urls')),
    path('notifications/', include('notifications.urls')),
]
