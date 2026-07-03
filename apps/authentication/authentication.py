"""JWT authentication backend for DRF."""
import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from apps.access.models import User
from apps.authentication.models import BlacklistedToken


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return None
        token = auth_header.split(' ', 1)[1]
        if BlacklistedToken.objects.filter(token=token).exists():
            raise AuthenticationFailed('Token blacklisted')
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')
        user = User.objects.filter(id=payload.get('user_id')).first()
        if not user or not user.is_active:
            raise AuthenticationFailed('User not found or inactive')
        return (user, token)

    def authenticate_header(self, request):
        return 'Bearer'
