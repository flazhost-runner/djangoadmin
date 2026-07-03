import os
import uuid
from django.conf import settings as django_settings
from .i_setting_service import ISettingService
from apps.setting.models import Setting
from core.errors import AppError
from core.helpers import remove_empty_fields

FILE_FIELDS = ('logo', 'login_image', 'icon', 'favicon')


class SettingService(ISettingService):
    def get(self) -> Setting:
        return Setting.objects.first()

    def update(self, data: dict, files=None, actor_id: str = '') -> Setting:
        setting = Setting.objects.first()
        if not setting:
            from core.errors import NotFoundError
            raise NotFoundError('Setting not found')
        data = remove_empty_fields(data)
        data['updated_by'] = actor_id
        for k, v in data.items():
            if k not in FILE_FIELDS and hasattr(setting, k):
                setattr(setting, k, v)

        if files:
            for field in FILE_FIELDS:
                f = files.get(field)
                if f and f.size > 0:
                    ext = os.path.splitext(f.name)[1].lower()
                    name = f'{uuid.uuid4().hex}{ext}'
                    subdir = os.path.join(django_settings.MEDIA_ROOT, 'setting')
                    os.makedirs(subdir, exist_ok=True)
                    path = os.path.join(subdir, name)
                    with open(path, 'wb') as out:
                        for chunk in f.chunks():
                            out.write(chunk)
                    url = f'{django_settings.MEDIA_URL}setting/{name}'
                    if hasattr(setting, field):
                        setattr(setting, field, url)

        setting.save()
        return setting
