import os
import uuid
from django.conf import settings as django_settings
from apps.access.models import User
from core.errors import NotFoundError, ConflictError
from core.helpers import remove_empty_fields
from django.contrib.auth.hashers import make_password, check_password

# Fields a user may set on their own profile. `picture` is written from the
# uploaded file, never from a raw text value; `email` is immutable here.
_PROFILE_FIELDS = {'name', 'phone', 'timezone', 'password', 'picture', 'updated_by'}


class ProfileService:
    def get(self, user_id: str) -> User:
        user = User.objects.prefetch_related('roles').filter(id=user_id).first()
        if not user:
            raise NotFoundError('User not found')
        return user

    def update(self, user_id: str, data: dict, files=None, actor_id: str = '') -> User:
        user = User.objects.filter(id=user_id).first()
        if not user:
            raise NotFoundError('User not found')
        data = remove_empty_fields(data)
        if data.get('password'):
            data['password'] = make_password(data['password'])
        data.pop('email', None)  # email cannot be changed via profile
        data['updated_by'] = actor_id

        # Save an uploaded avatar the same way SettingService stores its images:
        # <MEDIA_ROOT>/access/<uuid>.<ext>, store the /media/... URL in the column.
        f = files.get('picture') if files else None
        if f and getattr(f, 'size', 0) > 0:
            ext = os.path.splitext(f.name)[1].lower()
            name = f'{uuid.uuid4().hex}{ext}'
            subdir = os.path.join(django_settings.MEDIA_ROOT, 'access')
            os.makedirs(subdir, exist_ok=True)
            with open(os.path.join(subdir, name), 'wb') as out:
                for chunk in f.chunks():
                    out.write(chunk)
            data['picture'] = f'{django_settings.MEDIA_URL}access/{name}'

        for k, v in data.items():
            if k in _PROFILE_FIELDS:
                setattr(user, k, v)
        user.save()
        return user
