from django.urls import path
from apps.dashboard.views.web_views import DashboardIndexView
urlpatterns = [
    path('dashboard', DashboardIndexView.as_view(), name='admin.v1.dashboard.index'),
]
