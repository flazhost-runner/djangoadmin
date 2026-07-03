from django.views import View
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import QueryDict
from core.permissions import RoutePermissionMixin
from core.errors import AppError
from apps.access.services.permission_service import PermissionService

def _svc():
    return PermissionService()

class PermissionIndexView(RoutePermissionMixin, View):
    def get(self, request):
        _svc().sync_from_routes()
        result = _svc().index(request.GET.dict())
        return render(request, 'be/default/access/permissions/index.html', {
            **result, 'filter': request.GET.dict(), 'full_url': request.get_full_path(),
        })

class PermissionCreateView(RoutePermissionMixin, View):
    def get(self, request):
        return render(request, 'be/default/access/permissions/create.html', {})

class PermissionStoreView(RoutePermissionMixin, View):
    def post(self, request):
        try:
            data = {
                'name': request.POST.get('name', ''),
                'guard_name': request.POST.get('guard_name', 'web'),
                'method': request.POST.get('method', ''),
                'status': request.POST.get('status', 'Active'),
                'desc': request.POST.get('desc') or request.POST.get('description', ''),
            }
            _svc().store(data, actor_id=request.user.id)
            messages.success(request, 'Create Permission Success.')
            return redirect('admin.v1.access.permission.index')
        except AppError as e:
            messages.error(request, e.message)
            return redirect('admin.v1.access.permission.create')

class PermissionEditView(RoutePermissionMixin, View):
    def get(self, request, id):
        data = _svc().edit(id)
        return render(request, 'be/default/access/permissions/edit.html', {'data': data})

class PermissionUpdateView(RoutePermissionMixin, View):
    def put(self, request, id):
        try:
            body = QueryDict(request.body)
            data = {
                'name': body.get('name', ''),
                'guard_name': body.get('guard_name', 'web'),
                'method': body.get('method', ''),
                'status': body.get('status', 'Active'),
                'desc': body.get('desc') or body.get('description', ''),
            }
            _svc().update(id, data, actor_id=request.user.id)
            messages.success(request, 'Update Permission Success.')
            return redirect('admin.v1.access.permission.index')
        except AppError as e:
            messages.error(request, e.message)
            return redirect('admin.v1.access.permission.edit', id=id)

class PermissionDeleteView(RoutePermissionMixin, View):
    def delete(self, request, id):
        try:
            _svc().delete(id)
            messages.success(request, 'Delete Permission Success.')
        except AppError as e:
            messages.error(request, e.message)
        return redirect('admin.v1.access.permission.index')

class PermissionDeleteSelectedView(RoutePermissionMixin, View):
    def post(self, request):
        ids = request.POST.getlist('selected[]')
        try:
            count = _svc().delete_selected(ids)
            messages.success(request, f'Deleted {count} permission(s).')
        except AppError as e:
            messages.error(request, e.message)
        return redirect('admin.v1.access.permission.index')

class PermissionSyncView(RoutePermissionMixin, View):
    def post(self, request):
        count = _svc().sync_from_routes()
        messages.success(request, f'Synced {count} new permissions from routes.')
        return redirect('admin.v1.access.permission.index')
