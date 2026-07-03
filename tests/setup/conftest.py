import pytest
from django.contrib.auth.hashers import make_password


@pytest.fixture(autouse=True)
def setup_db(db):
    """Auto-use: every test gets a clean DB with seed data."""
    from apps.access.models import User, Role, UsersRoles
    from apps.setting.models import Setting
    import uuid
    role = Role.objects.create(
        id=str(uuid.uuid4()), name='Administrator', status='Active',
    )
    user = User.objects.create(
        id=str(uuid.uuid4()), code='ADM001', name='Administrator',
        email='admin@admin.com', password=make_password('12345678'),
        status='Active', blocked=False,
    )
    UsersRoles.objects.create(user=user, role=role)
    Setting.objects.create(
        id=str(uuid.uuid4()), name='Test App', theme='Blue',
    )
    yield


@pytest.fixture
def admin_user():
    from apps.access.models import User
    return User.objects.filter(email='admin@admin.com').first()


@pytest.fixture
def admin_client(client, admin_user):
    client.force_login(admin_user)
    return client
