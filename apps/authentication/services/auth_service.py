import random
import re
import time

import jwt
from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password

from apps.access.models import User
from apps.authentication.models import BlacklistedToken, hash_token
from core.errors import AppError, NotFoundError, UnauthorizedError

from .i_auth_service import IAuthService


def _parse_expires_in(value: str) -> int:
    """Parse JWT_EXPIRES_IN string like '1h', '30m', '7d' → seconds."""
    m = re.fullmatch(r'(\d+)([smhd]?)', value.strip().lower())
    if not m:
        return 3600
    n, unit = int(m.group(1)), m.group(2) or 's'
    return n * {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}[unit]


def _generate_token(user: User) -> str:
    expires_seconds = _parse_expires_in(getattr(settings, 'JWT_EXPIRES_IN', '1h'))
    payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': int(time.time()) + expires_seconds,
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')


class AuthService(IAuthService):
    def login(self, email: str, password: str) -> dict:
        user = User.objects.prefetch_related('roles').filter(email=email).first()
        if not user or not check_password(password, user.password):
            raise UnauthorizedError('Invalid credentials')
        if not user.is_active:
            raise UnauthorizedError('Account is inactive or blocked')
        token = _generate_token(user)
        return {'user': user, 'token': token}

    def register(self, data: dict) -> dict:
        from core.errors import ConflictError
        if User.objects.filter(email=data.get('email', '')).exists():
            raise ConflictError('Email already exists.')
        import uuid as _uuid
        user = User.objects.create(
            id=str(_uuid.uuid4()),
            email=data['email'],
            name=data.get('name', ''),
            password=make_password(data['password']),
            status='Active',
        )
        token = _generate_token(user)
        return {'user': user, 'token': token}

    def logout(self, token: str) -> None:
        BlacklistedToken.objects.get_or_create(token_hash=hash_token(token))

    def me(self, user) -> dict:
        return {'id': user.id, 'email': user.email, 'name': user.name, 'status': user.status}

    def request_reset(self, email: str) -> str:
        user = User.objects.filter(email=email).first()
        if not user:
            raise NotFoundError('Email not found.')
        otp = str(random.randint(0, 999999)).zfill(6)
        expiry_minutes = getattr(settings, 'OTP_EXPIRY_MINUTES', 10)
        user.password_otp = make_password(otp)
        user.password_otp_expires = int(time.time()) + int(expiry_minutes) * 60
        user.save(update_fields=['password_otp', 'password_otp_expires'])
        return otp

    def process_reset(self, email: str, otp: str, new_password: str) -> None:
        user = User.objects.filter(email=email).first()
        if not user or not user.password_otp:
            raise NotFoundError('Invalid request')
        if user.password_otp_expires and int(time.time()) > user.password_otp_expires:
            raise AppError('OTP has expired.', 422)
        if not check_password(otp, user.password_otp):
            raise AppError('OTP is invalid.', 422)
        user.password = make_password(new_password)
        user.password_otp = None
        user.password_otp_expires = None
        user.save(update_fields=['password', 'password_otp', 'password_otp_expires'])
