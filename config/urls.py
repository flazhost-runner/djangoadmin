from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Home (landing)
    path('', include('apps.home.urls.web')),
    # Auth (web)
    path('', include('apps.authentication.urls.web')),
    # Admin web routes
    path('admin/v1/', include('apps.access.urls.web')),
    path('admin/v1/', include('apps.dashboard.urls.web')),
    path('admin/v1/', include('apps.setting.urls.web')),
    path('admin/v1/', include('apps.profile.urls.web')),
    path('admin/v1/', include('apps.components.urls.web')),
    path('admin/v1/', include('apps.media.urls.web')),
    # API routes
    path('api/v1/', include('apps.authentication.urls.api')),
    path('api/v1/', include('apps.access.urls.api')),
    path('api/v1/', include('apps.setting.urls.api')),
    path('api/v1/', include('apps.profile.urls.api')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
