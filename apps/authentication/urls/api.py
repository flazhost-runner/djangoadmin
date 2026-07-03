from django.urls import path
from apps.authentication.views.api_views import (
    ApiLoginView, ApiLogoutView, ApiMeView, ApiRegisterView,
    ApiResetRequestView, ApiResetProcessView,
)
urlpatterns = [
    path('auth/login', ApiLoginView.as_view(), name='api.v1.auth.login'),
    path('auth/logout', ApiLogoutView.as_view(), name='api.v1.auth.logout'),
    path('auth/me', ApiMeView.as_view(), name='api.v1.auth.me'),
    path('auth/register', ApiRegisterView.as_view(), name='api.v1.auth.register'),
    path('auth/reset/request', ApiResetRequestView.as_view(), name='api.v1.auth.reset.request'),
    path('auth/reset/process', ApiResetProcessView.as_view(), name='api.v1.auth.reset.process'),
]
