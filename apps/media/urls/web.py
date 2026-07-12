from django.urls import path
from apps.media.views.web_views import (
    MediaListView, MediaUploadView, MediaDeleteView,
)

# Rich-text editor file manager (web — session auth + CSRF). Mounted under
# `admin/v1/` by config/urls.py, matching NodeAdmin's /admin/v1/media/* routes
# and the trumbowyg filemanager.js BASE ('/admin/v1/media').
urlpatterns = [
    path('media/list', MediaListView.as_view(), name='web.media.list'),
    path('media/upload', MediaUploadView.as_view(), name='web.media.upload'),
    path('media/delete', MediaDeleteView.as_view(), name='web.media.delete'),
]
