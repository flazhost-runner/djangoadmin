from django.urls import path
from apps.setting.views.api_views import ApiSettingIndex, ApiSettingUpdate
urlpatterns = [
    path('setting', ApiSettingIndex.as_view(), name='api.v1.setting.index'),
    path('setting/update', ApiSettingUpdate.as_view(), name='api.v1.setting.update'),
]
