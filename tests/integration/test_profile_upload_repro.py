"""Regression: profile picture upload via multipart + ?_method=PUT must not 500.

The old view re-parsed request.body, which raises RawPostDataException on a
multipart upload (MethodOverrideMiddleware already consumed the stream while the
method was still POST). Reading request.POST/FILES instead fixes it and also
lets the avatar actually be stored.
"""
import io
import uuid
import pytest
from django.contrib.auth.hashers import make_password
from apps.access.models import User, Role, UsersRoles


@pytest.fixture
def admin_web_client(client):
    """A freshly-built admin, linked to an Administrator role, logged in via web.
    Self-contained so it doesn't depend on the shared seed fixture."""
    role, _ = Role.objects.get_or_create(
        name='Administrator', defaults={'id': str(uuid.uuid4()), 'status': 'Active'})
    user = User.objects.create(
        id=str(uuid.uuid4()), code=f'A{uuid.uuid4().hex[:6]}', name='Admin',
        email=f'{uuid.uuid4().hex}@admin.com', password=make_password('12345678'),
        status='Active', blocked=False,
    )
    UsersRoles.objects.create(user=user, role=role)
    assert user.is_administrator()
    client.force_login(user)
    return client, user


@pytest.mark.django_db
class TestProfileUpload:
    def _png(self):
        f = io.BytesIO(b'\x89PNG\r\n\x1a\n' + b'0' * 64)
        f.name = 'avatar.png'
        return f

    def test_upload_picture_does_not_500(self, admin_web_client):
        client, user = admin_web_client
        resp = client.post(
            '/admin/v1/profile/update?_method=PUT',
            data={'name': 'Nama Baru', 'picture': self._png()},
        )
        assert resp.status_code == 302, resp.status_code
        user.refresh_from_db()
        assert user.name == 'Nama Baru'
        assert user.picture and user.picture.startswith('/media/access/'), user.picture

    def test_update_without_file_still_works(self, admin_web_client):
        client, user = admin_web_client
        resp = client.post(
            '/admin/v1/profile/update?_method=PUT',
            data={'name': 'Tanpa File', 'phone': '0811'},
        )
        assert resp.status_code == 302
        user.refresh_from_db()
        assert user.name == 'Tanpa File'
        assert user.phone == '0811'
