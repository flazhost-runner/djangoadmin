"""Test helpers."""
from django.test import Client


def login_web(client: Client, email='admin@admin.com', password='12345678') -> Client:
    client.post('/auth/login', {'email': email, 'password': password})
    return client


def get_csrf(client: Client, url='/auth/login') -> str:
    response = client.get(url)
    return client.cookies.get('csrftoken', None) or ''
