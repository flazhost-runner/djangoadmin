from apps.access.models import User
from core.errors import NotFoundError, ConflictError
from core.helpers import remove_empty_fields
from django.contrib.auth.hashers import make_password, check_password


class ProfileService:
    def get(self, user_id: str) -> User:
        user = User.objects.prefetch_related('roles').filter(id=user_id).first()
        if not user:
            raise NotFoundError('User not found')
        return user

    def update(self, user_id: str, data: dict, actor_id: str = '') -> User:
        user = User.objects.filter(id=user_id).first()
        if not user:
            raise NotFoundError('User not found')
        data = remove_empty_fields(data)
        if data.get('password'):
            data['password'] = make_password(data['password'])
        data.pop('email', None)  # email cannot be changed via profile
        data['updated_by'] = actor_id
        for k, v in data.items():
            setattr(user, k, v)
        user.save()
        return user
