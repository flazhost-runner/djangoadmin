from .i_role_service import IRoleService
from apps.access.models import Role, Permission, RolesPermissions
from core.helpers import paginate, ci_like, remove_empty_fields
from core.errors import NotFoundError, ConflictError, AppError


class RoleService(IRoleService):
    def index(self, params: dict) -> dict:
        qs = Role.objects.order_by('-created_at')
        if params.get('q_name'):
            qs = ci_like(qs, 'name', params['q_name'])
        if params.get('q_status'):
            qs = qs.filter(status=params['q_status'])
        if params.get('q_desc'):
            qs = ci_like(qs, 'desc', params['q_desc'])
        return paginate(qs, params)

    def store(self, data: dict, actor_id: str = '') -> Role:
        if Role.objects.filter(name=data.get('name', '')).exists():
            raise ConflictError('Role Already Exists')
        data = remove_empty_fields(data)
        data['created_by'] = actor_id
        data['updated_by'] = actor_id
        role = Role.objects.create(**data)
        if not role:
            raise AppError('Store Role Fail', 500)
        return role

    def edit(self, role_id: str) -> Role:
        role = Role.objects.filter(id=role_id).first()
        if not role:
            raise NotFoundError('Role not found')
        return role

    def update(self, role_id: str, data: dict, actor_id: str = '') -> Role:
        role = Role.objects.filter(id=role_id).first()
        if not role:
            raise NotFoundError('Role not found')
        data = remove_empty_fields(data)
        data['updated_by'] = actor_id
        for k, v in data.items():
            setattr(role, k, v)
        role.save()
        return role

    def delete(self, role_id: str) -> None:
        role = Role.objects.filter(id=role_id).first()
        if not role:
            raise NotFoundError('Role not found')
        role.delete()

    def delete_selected(self, ids: list) -> int:
        count, _ = Role.objects.filter(id__in=ids).delete()
        return count

    def get_permissions(self, role_id: str, params: dict) -> dict:
        role = Role.objects.filter(id=role_id).first()
        if not role:
            raise NotFoundError('Role not found')
        qs = Permission.objects.annotate_assigned(role_id) if hasattr(Permission.objects, 'annotate_assigned') else Permission.objects.all()
        # fallback: return all permissions with assigned flag
        assigned_ids = set(RolesPermissions.objects.filter(role_id=role_id).values_list('permission_id', flat=True))
        qs = Permission.objects.order_by('name')
        if params.get('q_name'):
            qs = ci_like(qs, 'name', params['q_name'])
        if params.get('q_status'):
            qs = qs.filter(status=params['q_status'])
        if params.get('q_desc'):
            qs = ci_like(qs, 'desc', params['q_desc'])
        result = paginate(qs, params)
        for p in result['datas']:
            p.assigned = p.id in assigned_ids
        return {**result, 'role': role}

    def assign_permission(self, role_id: str, perm_id: str, actor_id: str = '') -> None:
        role = Role.objects.filter(id=role_id).first()
        if not role:
            raise NotFoundError('Role not found')
        perm = Permission.objects.filter(id=perm_id).first()
        if not perm:
            raise NotFoundError('Permission not found')
        RolesPermissions.objects.get_or_create(role=role, permission=perm)

    def unassign_permission(self, role_id: str, perm_id: str) -> None:
        RolesPermissions.objects.filter(role_id=role_id, permission_id=perm_id).delete()

    def assign_selected(self, role_id: str, perm_ids: list) -> None:
        for pid in perm_ids:
            RolesPermissions.objects.get_or_create(role_id=role_id, permission_id=pid)

    def unassign_selected(self, role_id: str, perm_ids: list) -> None:
        RolesPermissions.objects.filter(role_id=role_id, permission_id__in=perm_ids).delete()
