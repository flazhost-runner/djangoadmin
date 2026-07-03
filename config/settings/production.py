import environ
from pathlib import Path
environ.Env.read_env(Path(__file__).resolve().parent.parent.parent / '.env')
from .base import *  # noqa: F401, F403
from .base import env  # noqa: F401
DEBUG = False
SECURE_HSTS_SECONDS = 31536000
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
