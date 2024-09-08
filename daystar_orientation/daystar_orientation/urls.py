from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FLUTTER_WEB_APP = os.path.join(BASE_DIR, "web")


def flutter_redirect(request, resource):
    return serve(request, resource, FLUTTER_WEB_APP)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('orientation/', include('orientation.urls')),
    path('account/', include('account.urls')),
    path('faqs/', include('faqs.urls')),
    path('activities/', include('activities.urls')),
    path('notifications/', include('notifications.urls')),
    path("", lambda r: flutter_redirect(r, "index.html")),
    path("<path:resource>", flutter_redirect),
    path('hods/', include('hods.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])