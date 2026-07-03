"""Base settings - environment-agnostic. Env file read by child settings before importing this."""
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ['localhost']),
    SECRET_KEY=(str, 'change-me'),
    SESSION_TTL_HOURS=(int, 6),
    DB_ENGINE=(str, 'django.db.backends.sqlite3'),
    DB_NAME=(str, 'db.sqlite3'),
    DB_USERNAME=(str, ''),
    DB_USER=(str, ''),
    DB_PASSWORD=(str, ''),
    DB_HOST=(str, ''),
    DB_PORT=(str, ''),
    JWT_SECRET=(str, 'change-me-jwt'),
    JWT_EXPIRES_IN=(str, '1h'),
    BCRYPT_ROUNDS=(int, 10),
    OTP_EXPIRY_MINUTES=(int, 10),
    DEFAULT_PAGE_SIZE=(int, 10),
    STORAGE_DRIVER=(str, 'local'),
    STORAGE_ACCESS_KEY_ID=(str, ''),
    STORAGE_SECRET_ACCESS_KEY=(str, ''),
    STORAGE_ENDPOINT=(str, ''),
    STORAGE_BUCKET=(str, ''),
    STORAGE_REGION=(str, ''),
    STORAGE_SSL=(bool, True),
    MAIL_HOST=(str, ''),
    MAIL_PORT=(int, 587),
    MAIL_SECURE=(bool, False),
    MAIL_USERNAME=(str, ''),
    MAIL_PASSWORD=(str, ''),
    MAIL_FROM_NAME=(str, 'DjangoAdmin'),
    MAIL_FROM_ADDRESS=(str, ''),
    REDIS_URL=(str, 'redis://127.0.0.1:6379'),
    SESSION_DRIVER=(str, 'database'),
    APP_NAME=(str, 'DjangoAdmin'),
    FE_TEMPLATE=(str, 'agency-consulting-002-creative-agency'),
)

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env('ALLOWED_HOSTS')

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'core',
    'apps.access',
    'apps.authentication',
    'apps.setting',
    'apps.dashboard',
    'apps.profile',
    'apps.components',
    'apps.home',
    'apps.media',
]

APPEND_SLASH = False

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'core.middleware.MethodOverrideMiddleware',
    'django.middleware.common.CommonMiddleware',
    'core.middleware.MultiSourceCsrfMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.theme_context',
                'core.context_processors.setting_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

_db_name = env('DB_NAME', default='db.sqlite3')
_db_user = env('DB_USERNAME', default='') or env('DB_USER', default='')
DATABASES = {
    'default': {
        'ENGINE': env('DB_ENGINE'),
        'NAME': ':memory:' if _db_name == ':memory:' else (BASE_DIR / _db_name if env('DB_ENGINE') == 'django.db.backends.sqlite3' else _db_name),
        'USER': _db_user,
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

AUTH_USER_MODEL = 'access.User'
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

_session_driver = env('SESSION_DRIVER')
if _session_driver == 'redis':
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
    SESSION_CACHE_ALIAS = 'default'
else:
    SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_TTL_HOURS = env('SESSION_TTL_HOURS')
SESSION_COOKIE_AGE = SESSION_TTL_HOURS * 3600
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'apps.authentication.authentication.JWTAuthentication',
    ],
    'EXCEPTION_HANDLER': 'core.exceptions.custom_exception_handler',
    'DEFAULT_PERMISSION_CLASSES': [],
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'storage'

FILE_UPLOAD_MAX_MEMORY_SIZE = 2 * 1024 * 1024
DATA_UPLOAD_MAX_MEMORY_SIZE = 2 * 1024 * 1024

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JWT_SECRET = env('JWT_SECRET')
JWT_EXPIRES_IN = env('JWT_EXPIRES_IN')
BCRYPT_ROUNDS = env('BCRYPT_ROUNDS')
OTP_EXPIRY_MINUTES = env('OTP_EXPIRY_MINUTES')
DEFAULT_PAGE_SIZE = env('DEFAULT_PAGE_SIZE')
STORAGE_DRIVER = env('STORAGE_DRIVER')
STORAGE_ACCESS_KEY_ID = env('STORAGE_ACCESS_KEY_ID')
STORAGE_SECRET_ACCESS_KEY = env('STORAGE_SECRET_ACCESS_KEY')
STORAGE_ENDPOINT = env('STORAGE_ENDPOINT')
STORAGE_BUCKET = env('STORAGE_BUCKET')
STORAGE_REGION = env('STORAGE_REGION')
STORAGE_SSL = env('STORAGE_SSL')
MAIL_HOST = env('MAIL_HOST')
MAIL_PORT = env('MAIL_PORT')
MAIL_SECURE = env('MAIL_SECURE')
MAIL_USERNAME = env('MAIL_USERNAME')
MAIL_PASSWORD = env('MAIL_PASSWORD')
MAIL_FROM_NAME = env('MAIL_FROM_NAME')
MAIL_FROM_ADDRESS = env('MAIL_FROM_ADDRESS')
REDIS_URL = env('REDIS_URL')
APP_NAME = env('APP_NAME')
FE_TEMPLATE = env('FE_TEMPLATE')

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = ['http://localhost:8000', 'http://127.0.0.1:8000']
WHITENOISE_USE_FINDERS = True

THEMES = {
    'Blue':   {'primary': '#3B82F6', 'secondary': '#60A5FA', 'light': '#EFF6FF', 'dark': '#1E40AF'},
    'Purple': {'primary': '#8B5CF6', 'secondary': '#A78BFA', 'light': '#F5F3FF', 'dark': '#5B21B6'},
    'Green':  {'primary': '#10B981', 'secondary': '#34D399', 'light': '#ECFDF5', 'dark': '#065F46'},
    'Orange': {'primary': '#F59E0B', 'secondary': '#FCD34D', 'light': '#FFFBEB', 'dark': '#92400E'},
    'Red':    {'primary': '#EF4444', 'secondary': '#F87171', 'light': '#FEF2F2', 'dark': '#991B1B'},
}

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
]

SETTING_CACHE_TTL = 60
