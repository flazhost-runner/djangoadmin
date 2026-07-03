"""Seed admin user + Administrator role."""
from django.db import migrations
import uuid


def seed_admin(apps, schema_editor):
    User = apps.get_model('access', 'User')
    Role = apps.get_model('access', 'Role')
    UsersRoles = apps.get_model('access', 'UsersRoles')

    from django.contrib.auth.hashers import make_password
    from django.utils import timezone as tz
    role, _ = Role.objects.get_or_create(
        name='Administrator',
        defaults={
            'id': str(uuid.uuid4()),
            'status': 'Active',
            'desc': '',
        },
    )
    user, created = User.objects.get_or_create(
        email='admin@admin.com',
        defaults={
            'id': str(uuid.uuid4()),
            'code': '0000000001',
            'name': 'Administrator',
            'phone': '12345678910',
            'email_verified_at': tz.now(),
            'password': make_password('12345678'),
            'status': 'Active',
            'timezone': 'Asia/Jakarta',
            'blocked': False,
            'blocked_reason': '',
        },
    )
    if created or not UsersRoles.objects.filter(user=user, role=role).exists():
        UsersRoles.objects.get_or_create(user=user, role=role)

    # Seed default setting
    Setting = apps.get_model('setting', 'Setting')
    if not Setting.objects.exists():
        Setting.objects.create(
            id=str(uuid.uuid4()),
            name='DjangoAdmin',
            initial='DA',
            theme='Blue',
            copyright='© 2024 DjangoAdmin',
        )


def unseed(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('access', '0001_initial'),
        ('setting', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(seed_admin, unseed),
    ]
