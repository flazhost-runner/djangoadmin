import environ
from pathlib import Path
environ.Env.read_env(Path(__file__).resolve().parent.parent.parent / '.env.test')
from .base import *  # noqa: F401, F403
from .base import env  # noqa: F401
DEBUG = True
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}}
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
CACHES = {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}}
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']
