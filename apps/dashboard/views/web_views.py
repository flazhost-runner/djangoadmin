from django.views import View
from django.shortcuts import render, redirect
from core.permissions import RoutePermissionMixin
from apps.dashboard.services.dashboard_service import DashboardService


class DashboardIndexView(RoutePermissionMixin, View):
    def get(self, request):
        stats = DashboardService().get_stats()
        return render(request, 'be/default/dashboard/index.html', {'stats': stats})
