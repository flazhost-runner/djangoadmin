import pytest
from django.test import Client


@pytest.mark.django_db
class TestAuthApi:
    def test_login_success(self, client):
        response = client.post('/api/v1/auth/login/', {
            'email': 'admin@admin.com',
            'password': '12345678',
        }, content_type='application/json')
        assert response.status_code == 200
        data = response.json()
        assert data['status'] is True
        assert 'token' in data['data']

    def test_login_fail(self, client):
        response = client.post('/api/v1/auth/login/', {
            'email': 'wrong@test.com',
            'password': 'wrongpassword',
        }, content_type='application/json')
        assert response.status_code == 401

    def test_me_requires_auth(self, client):
        response = client.get('/api/v1/auth/me/')
        assert response.status_code in [401, 403]

    def test_me_with_token(self, client):
        login = client.post('/api/v1/auth/login/', {
            'email': 'admin@admin.com', 'password': '12345678',
        }, content_type='application/json')
        token = login.json()['data']['token']
        me = client.get('/api/v1/auth/me/', HTTP_AUTHORIZATION=f'Bearer {token}')
        assert me.status_code == 200
