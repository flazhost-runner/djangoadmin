from django.views import View
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpRequest
from core.permissions import RoutePermissionMixin
from core.errors import AppError
from apps.access.services.user_service import UserService
from apps.access.models import Role


def _svc():
    return UserService()


class UserIndexView(RoutePermissionMixin, View):
    def get(self, request: HttpRequest):
        from django.shortcuts import render
        result = _svc().index(request.GET.dict())
        roles = Role.objects.filter(status='Active').order_by('name')
        return render(request, 'be/default/access/users/index.html', {
            **result, 'filter': request.GET.dict(), 'roles': roles,
            'full_url': request.get_full_path(),
        })


class UserCreateView(RoutePermissionMixin, View):
    def get(self, request: HttpRequest):
        from django.shortcuts import render
        roles = Role.objects.filter(status='Active').order_by('name')
        from core.helpers import get_timezones
        return render(request, 'be/default/access/users/create.html', {
            'roles': roles, 'timezones': get_timezones(),
        })


class UserStoreView(RoutePermissionMixin, View):
    def post(self, request: HttpRequest):
        try:
            data = request.POST.dict()
            data.pop('csrfmiddlewaretoken', None)
            data['roles'] = request.POST.getlist('roles[]')
            data.pop('roles[]', None)
            data.pop('password_confirmation', None)
            if data.get('blocked') == '1':
                data['blocked'] = True
            else:
                data['blocked'] = False
            _svc().store(data, actor_id=request.user.id)
            messages.success(request, 'Create User Success.')
            return redirect('admin.v1.access.user.index')
        except AppError as e:
            messages.error(request, e.message)
            request.session['form_errors'] = {}
            request.session['form_old'] = request.POST.dict()
            return redirect('admin.v1.access.user.create')


class UserEditView(RoutePermissionMixin, View):
    def get(self, request: HttpRequest, id: str):
        from django.shortcuts import render
        data = _svc().edit(id)
        roles = Role.objects.filter(status='Active').order_by('name')
        user_role_ids = list(data.roles.values_list('id', flat=True))
        from core.helpers import get_timezones
        return render(request, 'be/default/access/users/edit.html', {
            'data': data, 'roles': roles, 'user_role_ids': user_role_ids,
            'timezones': get_timezones(),
        })


class UserUpdateView(RoutePermissionMixin, View):
    def put(self, request: HttpRequest, id: str):
        try:
            from django.http import QueryDict
            body = QueryDict(request.body, mutable=True)
            data = body.dict()
            data.pop('csrfmiddlewaretoken', None)
            data['roles'] = body.getlist('roles[]')
            data.pop('roles[]', None)
            data.pop('password_confirmation', None)
            data['blocked'] = data.get('blocked') == '1'
            _svc().update(id, data, actor_id=request.user.id)
            messages.success(request, 'Update User Success.')
            return redirect('admin.v1.access.user.index')
        except AppError as e:
            messages.error(request, e.message)
            return redirect('admin.v1.access.user.edit', id=id)


class UserDeleteView(RoutePermissionMixin, View):
    def delete(self, request: HttpRequest, id: str):
        try:
            _svc().delete(id)
            messages.success(request, 'Delete User Success.')
        except AppError as e:
            messages.error(request, e.message)
        return redirect('admin.v1.access.user.index')


class UserDeleteSelectedView(RoutePermissionMixin, View):
    def post(self, request: HttpRequest):
        ids = request.POST.getlist('selected[]')
        try:
            count = _svc().delete_selected(ids)
            messages.success(request, f'Deleted {count} user(s).')
        except AppError as e:
            messages.error(request, e.message)
        return redirect('admin.v1.access.user.index')
