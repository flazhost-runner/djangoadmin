from .i_permission_service import IPermissionService
from apps.access.models import Permission
from core.helpers import paginate, ci_like, remove_empty_fields
from core.errors import NotFoundError, AppError


class PermissionService(IPermissionService):
    def index(self, params: dict) -> dict:
        qs = Permission.objects.order_by('name')
        if params.get('q_name'):
            qs = ci_like(qs, 'name', params['q_name'])
        if params.get('q_status'):
            qs = qs.filter(status=params['q_status'])
        if params.get('q_guard'):
            qs = qs.filter(guard_name=params['q_guard'])
        if params.get('q_method'):
            qs = ci_like(qs, 'method', params['q_method'])
        if params.get('q_desc'):
            qs = ci_like(qs, 'desc', params['q_desc'])
        return paginate(qs, params)

    def store(self, data: dict, actor_id: str = '') -> Permission:
        data = remove_empty_fields(data)
        data['created_by'] = actor_id
        data['updated_by'] = actor_id
        perm = Permission.objects.create(**data)
        if not perm:
            raise AppError('Store Permission Fail', 500)
        return perm

    def edit(self, perm_id: str) -> Permission:
        perm = Permission.objects.filter(id=perm_id).first()
        if not perm:
            raise NotFoundError('Permission not found')
        return perm

    def update(self, perm_id: str, data: dict, actor_id: str = '') -> Permission:
        perm = Permission.objects.filter(id=perm_id).first()
        if not perm:
            raise NotFoundError('Permission not found')
        data = remove_empty_fields(data)
        data['updated_by'] = actor_id
        for k, v in data.items():
            setattr(perm, k, v)
        perm.save()
        return perm

    def delete(self, perm_id: str) -> None:
        perm = Permission.objects.filter(id=perm_id).first()
        if not perm:
            raise NotFoundError('Permission not found')
        perm.delete()

    def delete_selected(self, ids: list) -> int:
        count, _ = Permission.objects.filter(id__in=ids).delete()
        return count

    def sync_from_routes(self) -> int:
        from django.urls import get_resolver
        import uuid
        resolver = get_resolver()
        count = 0
        def walk(resolver_or_pattern, prefix=''):
            for pattern in resolver_or_pattern.url_patterns:
                if hasattr(pattern, 'url_patterns'):
                    walk(pattern, prefix)
                else:
                    name = getattr(pattern, 'name', None)
                    if name:
                        guard = 'api' if name.startswith('api.') else 'web'
                        for method in ['GET', 'POST', 'PUT', 'DELETE']:
                            _, created = Permission.objects.get_or_create(
                                name=name,
                                method=method,
                                defaults={'id': str(uuid.uuid4()), 'guard_name': guard, 'status': 'Active'},
                            )
                            if created:
                                nonlocal count
                                count += 1
        walk(resolver)
        return count
