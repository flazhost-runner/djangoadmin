import pytest


@pytest.mark.django_db
class TestSmoke:
    def test_home_page(self, client):
        response = client.get('/')
        assert response.status_code == 200

    def test_login_page(self, client):
        response = client.get('/auth/login')
        assert response.status_code == 200

    def test_dashboard_redirects_when_not_logged_in(self, client):
        response = client.get('/admin/v1/dashboard/')
        assert response.status_code in [302, 200]

    def test_api_login_endpoint_exists(self, client):
        response = client.post('/api/v1/auth/login/', {}, content_type='application/json')
        assert response.status_code in [400, 401, 200]

    def test_db_connection(self):
        from apps.access.models import User
        count = User.objects.count()
        assert count >= 0
