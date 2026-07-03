from django.views import View
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import HttpRequest, QueryDict
from core.permissions import RoutePermissionMixin
from core.errors import AppError
from apps.access.services.role_service import RoleService


def _svc():
    return RoleService()


class RoleIndexView(RoutePermissionMixin, View):
    def get(self, request):
        result = _svc().index(request.GET.dict())
        return render(request, 'be/default/access/roles/index.html', {
            **result, 'filter': request.GET.dict(), 'full_url': request.get_full_path(),
        })


class RoleCreateView(RoutePermissionMixin, View):
    def get(self, request):
        return render(request, 'be/default/access/roles/create.html', {})


class RoleStoreView(RoutePermissionMixin, View):
    def post(self, request):
        try:
            data = request.POST.dict()
            data.pop('csrfmiddlewaretoken', None)
            _svc().store(data, actor_id=request.user.id)
            messages.success(request, 'Create Role Success.')
            return redirect('admin.v1.access.role.index')
        except AppError as e:
            messages.error(request, e.message)
            return redirect('admin.v1.access.role.create')


class RoleEditView(RoutePermissionMixin, View):
    def get(self, request, id):
        data = _svc().edit(id)
        return render(request, 'be/default/access/roles/edit.html', {'data': data})


class RoleUpdateView(RoutePermissionMixin, View):
    def put(self, request, id):
        try:
            body = QueryDict(request.body)
            data = body.dict()
            data.pop('csrfmiddlewaretoken', None)
            _svc().update(id, data, actor_id=request.user.id)
            messages.success(request, 'Update Role Success.')
            return redirect('admin.v1.access.role.index')
        except AppError as e:
            messages.error(request, e.message)
            return redirect('admin.v1.access.role.edit', id=id)


class RoleDeleteView(RoutePermissionMixin, View):
    def delete(self, request, id):
        try:
            _svc().delete(id)
            messages.success(request, 'Delete Role Success.')
        except AppError as e:
            messages.error(request, e.message)
        return redirect('admin.v1.access.role.index')


class RoleDeleteSelectedView(RoutePermissionMixin, View):
    def post(self, request):
        ids = request.POST.getlist('selected[]')
        try:
            count = _svc().delete_selected(ids)
            messages.success(request, f'Deleted {count} role(s).')
        except AppError as e:
            messages.error(request, e.message)
        return redirect('admin.v1.access.role.index')


class RolePermissionView(RoutePermissionMixin, View):
    def get(self, request, id):
        result = _svc().get_permissions(id, request.GET.dict())
        return render(request, 'be/default/access/roles/permission.html', {
            **result, 'filter': request.GET.dict(), 'full_url': request.get_full_path(),
        })


class RolePermissionAssignView(RoutePermissionMixin, View):
    def post(self, request, id, perm_id):
        try:
            _svc().assign_permission(id, perm_id, actor_id=request.user.id)
            messages.success(request, 'Assign Permission Success.')
        except AppError as e:
            messages.error(request, e.message)
        return redirect('admin.v1.access.role.permission', id=id)


class RolePermissionUnassignView(RoutePermissionMixin, View):
    def post(self, request, id, perm_id):
        try:
            _svc().unassign_permission(id, perm_id)
            messages.success(request, 'Unassign Permission Success.')
        except AppError as e:
            messages.error(request, e.message)
        return redirect('admin.v1.access.role.permission', id=id)


class RolePermissionAssignSelectedView(RoutePermissionMixin, View):
    def post(self, request, id):
        perm_ids = request.POST.getlist('selected[]')
        try:
            _svc().assign_selected(id, perm_ids)
            messages.success(request, f'Assigned {len(perm_ids)} permission(s).')
        except AppError as e:
            messages.error(request, e.message)
        return redirect('admin.v1.access.role.permission', id=id)


class RolePermissionUnassignSelectedView(RoutePermissionMixin, View):
    def post(self, request, id):
        perm_ids = request.POST.getlist('selected[]')
        try:
            _svc().unassign_selected(id, perm_ids)
            messages.success(request, f'Unassigned {len(perm_ids)} permission(s).')
        except AppError as e:
            messages.error(request, e.message)
        return redirect('admin.v1.access.role.permission', id=id)
