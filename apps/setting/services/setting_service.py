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

        # Validate the FE template slug pattern before saving (anti-SSRF).
        from apps.home.services.fe_template_service import FeTemplateService
        fe_slug = data.get('fe_template')
        if fe_slug is not None and not FeTemplateService().is_valid_slug(fe_slug):
            raise AppError('Template tidak dikenali', 400)
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

        # Refresh the cached Setting so changes show up immediately.
        from core.context_processors import invalidate_setting_cache
        invalidate_setting_cache()

        # FE template changed → download on-demand (when not cached yet).
        # A failed download must not fail the save (landing falls back).
        if fe_slug:
            try:
                FeTemplateService().ensure(fe_slug)
            except AppError as e:
                import logging
                logging.getLogger(__name__).error('Unduh template frontend gagal: %s', e.message)

        return setting
