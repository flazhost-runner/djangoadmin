# DjangoAdmin starter kit — FlazHost PaaS (CapRover) build context.
#
# Single-stage image on python:3.12-slim (Django 6 requires Python >= 3.12).
# The container:
#   - runs `manage.py migrate` on boot (idempotent; includes the data
#     migration apps/access/migrations/0002_seed.py which seeds the
#     Administrator role + admin@admin.com / 12345678 via get_or_create)
#   - runs `manage.py collectstatic` (WhiteNoise serves the result)
#   - listens on $APP_PORT (default 80) for CapRover via gunicorn
#   - defaults to a zero-config SQLite DB under /app/data, while allowing a
#     managed DB purely via environment variables.
#
# No Redis is bundled: SESSION_DRIVER defaults to `database`, Django's cache
# defaults to locmem, and django-ratelimit is unused in app code.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Dependencies first for layer caching. All pinned deps (incl. Pillow 12 /
# bcrypt) ship manylinux wheels for cp312, so no build toolchain is needed.
# Extras NOT in requirements.txt (do not edit that file):
#   - gunicorn : production WSGI server (dev flow uses `runserver`)
#   - bcrypt   : required by PASSWORD_HASHERS[0] = BCryptSHA256PasswordHasher
#                (the seed migration calls make_password → would crash without it)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt gunicorn bcrypt

# App source.
COPY . .
RUN chmod +x /app/docker-entrypoint.sh \
 && mkdir -p /app/data /app/storage /app/staticfiles

# --- Defaults: zero-config boot, every value overridable via env ---
# ALLOWED_HOSTS=* is safe here: the container always sits behind the CapRover
# reverse proxy, which owns the public Host routing.
ENV DJANGO_SETTINGS_MODULE=config.settings.production \
    APP_PORT=80 \
    ALLOWED_HOSTS=* \
    DB_ENGINE=django.db.backends.sqlite3 \
    DB_NAME=/app/data/db.sqlite3 \
    SESSION_DRIVER=database

EXPOSE 80

ENTRYPOINT ["/app/docker-entrypoint.sh"]
