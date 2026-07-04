#!/bin/sh
# DjangoAdmin container boot sequence (FlazHost / CapRover):
#   1. map CapRover's $PORT -> APP_PORT
#   2. map platform DB_* envs -> the django-environ names used by settings
#   3. ensure mandatory secrets exist (generate + persist if not provided)
#   4. run migrations (idempotent; seeds admin@admin.com via data migration)
#   5. collectstatic for WhiteNoise
#   6. exec gunicorn on 0.0.0.0:$APP_PORT
set -eu

# --- 1. Port: CapRover injects $PORT (default 80) -----------------------------
: "${PORT:=80}"
export APP_PORT="${APP_PORT:-$PORT}"

# --- 2. Database env mapping ---------------------------------------------------
# Settings (config/settings/base.py) read DB_ENGINE / DB_NAME / DB_USERNAME /
# DB_PASSWORD / DB_HOST / DB_PORT via django-environ. The platform may inject
# the generic DB_TYPE / DB_DATABASE pair instead — translate when present.
if [ -n "${DB_TYPE:-}" ]; then
    case "$DB_TYPE" in
        sqlite|sqlite3|better-sqlite3) export DB_ENGINE="django.db.backends.sqlite3" ;;
        mysql|mariadb)                 export DB_ENGINE="django.db.backends.mysql" ;;
        postgres|postgresql|pg)        export DB_ENGINE="django.db.backends.postgresql" ;;
        *) echo "[entrypoint] WARN: unknown DB_TYPE='$DB_TYPE' — keeping DB_ENGINE=${DB_ENGINE:-unset}" ;;
    esac
fi
if [ -n "${DB_DATABASE:-}" ]; then
    export DB_NAME="$DB_DATABASE"
fi

# Default DB is SQLite under /app/data (writable; persists when /app/data is a
# mounted volume). Make sure its directory exists.
export DB_ENGINE="${DB_ENGINE:-django.db.backends.sqlite3}"
if [ "$DB_ENGINE" = "django.db.backends.sqlite3" ]; then
    export DB_NAME="${DB_NAME:-/app/data/db.sqlite3}"
    case "$DB_NAME" in
        /*) mkdir -p "$(dirname "$DB_NAME")" 2>/dev/null || true ;;
    esac
fi

# --- 3. Secrets (SECRET_KEY / JWT_SECRET) --------------------------------------
# Honour values supplied via the environment. Otherwise generate strong random
# secrets once and persist them so sessions/JWTs survive container restarts
# (persists across restarts when /app/data is a mounted volume).
DATA_DIR=/app/data
SECRETS_FILE="$DATA_DIR/.runtime-secrets"
mkdir -p "$DATA_DIR"

gen_secret() {
    python -c "import secrets; print(secrets.token_hex(32))"
}

[ -f "$SECRETS_FILE" ] && . "$SECRETS_FILE"

if [ -z "${SECRET_KEY:-}" ]; then
    SECRET_KEY="$(gen_secret)"
    echo "SECRET_KEY=$SECRET_KEY" >> "$SECRETS_FILE"
    echo "[entrypoint] Generated SECRET_KEY (persisted in $SECRETS_FILE)"
fi
if [ -z "${JWT_SECRET:-}" ]; then
    JWT_SECRET="$(gen_secret)"
    echo "JWT_SECRET=$JWT_SECRET" >> "$SECRETS_FILE"
    echo "[entrypoint] Generated JWT_SECRET (persisted in $SECRETS_FILE)"
fi
export SECRET_KEY JWT_SECRET

echo "[entrypoint] DB_ENGINE=$DB_ENGINE DB_NAME=${DB_NAME:-} APP_PORT=$APP_PORT SETTINGS=${DJANGO_SETTINGS_MODULE:-config.settings.production}"

# --- 4. Migrations (idempotent) ------------------------------------------------
# Includes the seed data migration (Administrator role + admin@admin.com /
# 12345678 + default Setting row, all via get_or_create). A failure here (e.g.
# transient managed-DB hiccup against an already-migrated schema) must NOT
# block boot — log and continue.
echo "[entrypoint] Running database migrations..."
if python manage.py migrate --noinput; then
    echo "[entrypoint] Migrations applied (admin seed included)."
else
    echo "[entrypoint] WARN: migrate exited non-zero — continuing to start server"
fi

# --- 5. Static files for WhiteNoise --------------------------------------------
echo "[entrypoint] Collecting static files..."
python manage.py collectstatic --noinput \
    || echo "[entrypoint] WARN: collectstatic failed — WhiteNoise finders will still serve static/"

# --- 6. Start gunicorn (PID 1 for clean SIGTERM/graceful shutdown) --------------
echo "[entrypoint] Starting gunicorn on 0.0.0.0:$APP_PORT"
exec gunicorn config.wsgi:application \
    --bind "0.0.0.0:$APP_PORT" \
    --workers "${GUNICORN_WORKERS:-2}" \
    --threads "${GUNICORN_THREADS:-4}" \
    --timeout "${GUNICORN_TIMEOUT:-60}" \
    --access-logfile - \
    --error-logfile -
