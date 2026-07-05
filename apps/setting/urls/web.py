from django.urls import path
from apps.setting.views.web_views import SettingIndexView, SettingUpdateView, SettingFePreviewView
urlpatterns = [
    path('setting', SettingIndexView.as_view(), name='admin.v1.setting.index'),
    path('setting/fe-preview/<slug:slug>', SettingFePreviewView.as_view(), name='admin.v1.setting.fe_preview'),
    path('setting/update', SettingUpdateView.as_view(), name='admin.v1.setting.update'),
]
