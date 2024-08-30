from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('orientation/', include('orientation.urls')),
    path('account/', include('account.urls')),
    path('faqs/', include('faqs.urls')),
    path('activities/', include('activities.urls')),
    path('notifications/', include('notifications.urls')),
    path('hods/', include('hods.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)