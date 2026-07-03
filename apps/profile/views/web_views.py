from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import QueryDict
from core.permissions import RoutePermissionMixin
from core.errors import AppError
from apps.profile.services.profile_service import ProfileService
from core.helpers import get_timezones


class ProfileIndexView(RoutePermissionMixin, View):
    def get(self, request):
        data = ProfileService().get(request.user.id)
        return render(request, 'be/default/profile/index.html', {'data': data, 'timezones': get_timezones()})


class ProfileUpdateView(RoutePermissionMixin, View):
    def put(self, request):
        try:
            body = QueryDict(request.body, mutable=True)
            data = body.dict()
            data.pop('csrfmiddlewaretoken', None)
            ProfileService().update(request.user.id, data, actor_id=request.user.id)
            messages.success(request, 'Update Profile Success.')
        except AppError as e:
            messages.error(request, e.message)
        return redirect('admin.v1.profile.index')
