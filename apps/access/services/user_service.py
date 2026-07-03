from .i_user_service import IUserService
from apps.access.models import User, Role, UsersRoles
from core.helpers import paginate, ci_like, remove_empty_fields
from core.errors import NotFoundError, ConflictError, AppError
from django.contrib.auth.hashers import make_password


_USER_FIELDS = {'code', 'name', 'phone', 'email', 'timezone', 'picture',
                'status', 'blocked', 'blocked_reason', 'password',
                'created_by', 'updated_by'}


class UserService(IUserService):
    def index(self, params: dict) -> dict:
        qs = User.objects.prefetch_related('roles').order_by('-created_at')
        if params.get('q_code'):
            qs = ci_like(qs, 'code', params['q_code'])
        if params.get('q_name'):
            qs = ci_like(qs, 'name', params['q_name'])
        if params.get('q_phone'):
            qs = ci_like(qs, 'phone', params['q_phone'])
        if params.get('q_email'):
            qs = ci_like(qs, 'email', params['q_email'])
        if params.get('q_status'):
            qs = qs.filter(status=params['q_status'])
        if params.get('q_role'):
            qs = qs.filter(users_roles__role_id=params['q_role'])
        return paginate(qs, params)

    def store(self, data: dict, actor_id: str = '') -> User:
        if User.objects.filter(email=data.get('email', '')).exists():
            raise ConflictError('User Already Exists')
        roles_ids = data.pop('roles', [])
        data = {k: v for k, v in remove_empty_fields(data).items() if k in _USER_FIELDS}
        if data.get('password'):
            data['password'] = make_password(data['password'])
        data['created_by'] = actor_id
        data['updated_by'] = actor_id
        user = User.objects.create(**data)
        if not user:
            raise AppError('Store User Fail', 500)
        for rid in roles_ids:
            UsersRoles.objects.get_or_create(user=user, role_id=rid)
        return user

    def edit(self, user_id: str) -> User:
        user = User.objects.prefetch_related('roles').filter(id=user_id).first()
        if not user:
            raise NotFoundError('User not found')
        return user

    def update(self, user_id: str, data: dict, actor_id: str = '') -> User:
        user = User.objects.filter(id=user_id).first()
        if not user:
            raise NotFoundError('User not found')
        roles_ids = data.pop('roles', None)
        data = {k: v for k, v in remove_empty_fields(data).items() if k in _USER_FIELDS}
        if data.get('password'):
            data['password'] = make_password(data['password'])
        data['updated_by'] = actor_id
        for k, v in data.items():
            setattr(user, k, v)
        user.save()
        if roles_ids is not None:
            UsersRoles.objects.filter(user=user).delete()
            for rid in roles_ids:
                UsersRoles.objects.get_or_create(user=user, role_id=rid)
        return user

    def delete(self, user_id: str) -> None:
        user = User.objects.filter(id=user_id).first()
        if not user:
            raise NotFoundError('User not found')
        user.delete()

    def delete_selected(self, ids: list) -> int:
        count, _ = User.objects.filter(id__in=ids).delete()
        return count
