from django.urls import path
from apps.profile.views.web_views import ProfileIndexView, ProfileUpdateView
urlpatterns = [
    path('profile', ProfileIndexView.as_view(), name='admin.v1.profile.index'),
    path('profile/update', ProfileUpdateView.as_view(), name='admin.v1.profile.update'),
]
