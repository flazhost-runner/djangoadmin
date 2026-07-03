from django.views import View
from django.shortcuts import render
from core.permissions import RoutePermissionMixin


class ComponentsIndexView(RoutePermissionMixin, View):
    def get(self, request):
        return render(request, 'be/default/components/index.html', {})
