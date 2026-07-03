from django.urls import path
from apps.setting.views.web_views import SettingIndexView, SettingUpdateView
urlpatterns = [
    path('setting', SettingIndexView.as_view(), name='admin.v1.setting.index'),
    path('setting/update', SettingUpdateView.as_view(), name='admin.v1.setting.update'),
]
