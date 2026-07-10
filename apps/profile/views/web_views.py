from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
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
            # Read the already-parsed request.POST/FILES (MethodOverrideMiddleware
            # parses the body while the method is still POST). Re-parsing
            # request.body here would raise RawPostDataException on a
            # multipart/form-data upload — the stream is already consumed — which
            # is what 500'd the picture upload.
            data = {k: v[0] if isinstance(v, list) and len(v) == 1 else v
                    for k, v in dict(request.POST).items()}
            data.pop('csrfmiddlewaretoken', None)
            ProfileService().update(request.user.id, data, files=request.FILES, actor_id=request.user.id)
            messages.success(request, 'Update Profile Success.')
        except AppError as e:
            messages.error(request, e.message)
        return redirect('admin.v1.profile.index')
