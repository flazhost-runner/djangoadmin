from django.urls import path
from apps.authentication.views.web_views import (
    LoginView, LogoutView, RegisterView, ResetRequestView, ResetProcessView,
)
urlpatterns = [
    path('auth/login', LoginView.as_view(), name='web.auth.login'),
    path('auth/login', LoginView.as_view(), name='web.auth.login.post'),
    path('auth/logout', LogoutView.as_view(), name='web.auth.logout'),
    path('auth/register', RegisterView.as_view(), name='web.auth.register'),
    path('auth/register/post', RegisterView.as_view(), name='web.auth.register.post'),
    path('auth/reset/request', ResetRequestView.as_view(), name='web.auth.reset.req'),
    path('auth/reset/request/post', ResetRequestView.as_view(), name='web.auth.reset.request'),
    path('auth/reset/process', ResetProcessView.as_view(), name='web.auth.reset.proc'),
    path('auth/reset/process/post', ResetProcessView.as_view(), name='web.auth.reset.process'),
]
