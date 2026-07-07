import environ
from pathlib import Path
environ.Env.read_env(Path(__file__).resolve().parent.parent.parent / '.env')
from .base import *  # noqa: F401, F403
from .base import env, ALLOWED_HOSTS  # noqa: F401
DEBUG = False
SECURE_HSTS_SECONDS = 31536000
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# Behind a TLS-terminating reverse proxy (e.g. CapRover): browser→proxy is HTTPS,
# proxy→app is HTTP with `X-Forwarded-Proto: https`. Trust that header so
# request.is_secure() is True — otherwise secure cookies aren't honoured and
# Django's CSRF origin check rejects the https Origin as a mismatch.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# Trust the https origin of each configured host for CSRF origin/referer checks.
CSRF_TRUSTED_ORIGINS = [f'https://{host}' for host in ALLOWED_HOSTS if host not in ('*', 'localhost', '127.0.0.1')]
