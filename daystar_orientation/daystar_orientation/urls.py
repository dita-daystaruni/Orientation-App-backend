from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('orientation/', include('orientation.urls')),
    path('account/', include('account.urls')),
    path('faqs/', include('faqs.urls')),
    path('activities/', include('activities.urls')),
    path('events/', include('events.urls')),
    path('notifications/', include('notifications.urls')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'), 
]
