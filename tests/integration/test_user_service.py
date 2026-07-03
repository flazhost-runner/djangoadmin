import pytest
from apps.access.services.user_service import UserService


@pytest.mark.django_db
class TestUserService:
    def test_index(self):
        svc = UserService()
        result = svc.index({})
        assert 'datas' in result
        assert len(result['datas']) >= 1  # admin seeded

    def test_store_and_reject_duplicate(self):
        svc = UserService()
        user = svc.store({'email': 'test@test.com', 'password': 'test1234', 'name': 'Test'})
        assert user.email == 'test@test.com'
        with pytest.raises(Exception):
            svc.store({'email': 'test@test.com', 'password': 'test1234'})

    def test_edit(self):
        svc = UserService()
        from apps.access.models import User
        u = User.objects.first()
        found = svc.edit(u.id)
        assert found.id == u.id

    def test_delete(self):
        svc = UserService()
        user = svc.store({'email': 'todel@test.com', 'password': 'test1234'})
        svc.delete(user.id)
        from apps.access.models import User
        assert not User.objects.filter(id=user.id).exists()

    def test_delete_not_found(self):
        from core.errors import NotFoundError
        svc = UserService()
        with pytest.raises(NotFoundError):
            svc.delete('nonexistent-id')
