from django.urls import path
from apps.profile.views.api_views import ProfileApiIndex

urlpatterns = [
    path('profile', ProfileApiIndex.as_view(), name='api.v1.profile.index'),
]
