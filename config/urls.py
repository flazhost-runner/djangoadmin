import re
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

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
]

# ---------------------------------------------------------------------------
# Local storage driver (STORAGE_DRIVER=local): serve uploaded media from the
# app itself. Mirrors NodeAdmin, which mounts the local storage dir on a stable
# URL prefix unconditionally so images render in every environment.
#
# Django's built-in `static()` helper only wires this up when DEBUG=True, which
# breaks media rendering in production. We register the serve route directly so
# uploaded files render under MEDIA_URL in prod too. For oss/s3 drivers the
# render URL is an absolute presigned/public URL (see get_file), so this route
# is simply never hit. Front with nginx/CDN for scale (see README).
# ---------------------------------------------------------------------------
if settings.STORAGE_DRIVER == 'local':
    _media_prefix = settings.MEDIA_URL.lstrip('/')
    urlpatterns += [
        re_path(
            r'^%s(?P<path>.*)$' % re.escape(_media_prefix),
            serve,
            {'document_root': settings.MEDIA_ROOT},
        ),
    ]
