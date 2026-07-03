"""Module generator — generates scaffold for a new DjangoAdmin app."""
import os
import uuid
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Generate a new DjangoAdmin module scaffold (models/services/views/urls/templates)'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Module name (e.g. product)')

    def handle(self, *args, **options):
        name = options['name'].lower()
        Name = name.capitalize()
        base = os.getcwd()
        app_dir = os.path.join(base, 'apps', name)

        if os.path.exists(app_dir):
            raise CommandError(f'App "{name}" already exists at {app_dir}')

        dirs = [
            app_dir,
            os.path.join(app_dir, 'migrations'),
            os.path.join(app_dir, 'services'),
            os.path.join(app_dir, 'views'),
            os.path.join(app_dir, 'urls'),
        ]
        for d in dirs:
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, '__init__.py'), 'w').close()

        # apps.py
        with open(os.path.join(app_dir, 'apps.py'), 'w') as f:
            f.write(f"""from django.apps import AppConfig
class {Name}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.{name}'
    label = '{name}'
""")

        # models.py
        with open(os.path.join(app_dir, 'models.py'), 'w') as f:
            f.write(f"""import uuid
from core.models import BaseModel
from django.db import models


class {Name}(BaseModel):
    class Meta:
        db_table = '{name}s'

    name = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=20, default='Active')

    def __str__(self):
        return self.name
""")

        # services/i_{name}_service.py
        with open(os.path.join(app_dir, 'services', f'i_{name}_service.py'), 'w') as f:
            f.write(f"""from abc import ABC, abstractmethod
class I{Name}Service(ABC):
    @abstractmethod
    def index(self, params: dict) -> dict: ...
    @abstractmethod
    def store(self, data: dict, actor_id: str = '') -> object: ...
    @abstractmethod
    def edit(self, id: str) -> object: ...
    @abstractmethod
    def update(self, id: str, data: dict, actor_id: str = '') -> object: ...
    @abstractmethod
    def delete(self, id: str) -> None: ...
    @abstractmethod
    def delete_selected(self, ids: list) -> int: ...
""")

        # services/{name}_service.py
        with open(os.path.join(app_dir, 'services', f'{name}_service.py'), 'w') as f:
            f.write(f"""from .i_{name}_service import I{Name}Service
from apps.{name}.models import {Name}
from core.helpers import paginate, ci_like, remove_empty_fields
from core.errors import NotFoundError, ConflictError, AppError


class {Name}Service(I{Name}Service):
    def index(self, params: dict) -> dict:
        qs = {Name}.objects.order_by('-created_at')
        if params.get('q_name'):
            qs = ci_like(qs, 'name', params['q_name'])
        if params.get('q_status'):
            qs = qs.filter(status=params['q_status'])
        return paginate(qs, params)

    def store(self, data: dict, actor_id: str = '') -> {Name}:
        if {Name}.objects.filter(name=data.get('name', '')).exists():
            raise ConflictError('{Name} Already Exists')
        data = remove_empty_fields(data)
        data['created_by'] = actor_id
        data['updated_by'] = actor_id
        obj = {Name}.objects.create(**data)
        if not obj:
            raise AppError('Store {Name} Fail', 500)
        return obj

    def edit(self, id: str) -> {Name}:
        obj = {Name}.objects.filter(id=id).first()
        if not obj:
            raise NotFoundError('{Name} not found')
        return obj

    def update(self, id: str, data: dict, actor_id: str = '') -> {Name}:
        obj = {Name}.objects.filter(id=id).first()
        if not obj:
            raise NotFoundError('{Name} not found')
        data = remove_empty_fields(data)
        data['updated_by'] = actor_id
        for k, v in data.items():
            setattr(obj, k, v)
        obj.save()
        return obj

    def delete(self, id: str) -> None:
        obj = {Name}.objects.filter(id=id).first()
        if not obj:
            raise NotFoundError('{Name} not found')
        obj.delete()

    def delete_selected(self, ids: list) -> int:
        count, _ = {Name}.objects.filter(id__in=ids).delete()
        return count
""")

        self.stdout.write(self.style.SUCCESS(f'Module "{name}" created at {app_dir}'))
        self.stdout.write(f'Next steps:')
        self.stdout.write(f'  1. Add "apps.{name}" to INSTALLED_APPS in config/settings/base.py')
        self.stdout.write(f'  2. python manage.py makemigrations {name}')
        self.stdout.write(f'  3. Create views in apps/{name}/views/')
        self.stdout.write(f'  4. Create URLs in apps/{name}/urls/')
        self.stdout.write(f'  5. Add templates in templates/be/default/{name}/')
