# DjangoAdmin

Django 6.0.6 + DRF 3.17.1 port of NodeAdmin. Modular admin panel with RBAC, JWT API, and multi-theme UI.

## Requirements

- Python 3.12+
- Git

## Installation

```bash
git clone <repo-url>
cd DjangoAdmin

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## Setup

```bash
cp .env.example .env.development
# Edit .env.development sesuai kebutuhan (DB, SECRET_KEY, dll.)
```

Jalankan migrasi dan seed data awal:

```bash
DJANGO_SETTINGS_MODULE=config.settings.development .venv/bin/python manage.py migrate
```

## Menjalankan App

```bash
DJANGO_SETTINGS_MODULE=config.settings.development .venv/bin/python manage.py runserver
```

Default berjalan di `http://localhost:8000`.

**Ubah port:**

```bash
DJANGO_SETTINGS_MODULE=config.settings.development .venv/bin/python manage.py runserver 8080
```

**Akses dari semua interface (misal VM/server):**

```bash
DJANGO_SETTINGS_MODULE=config.settings.development .venv/bin/python manage.py runserver 0.0.0.0:8080
```

## Akun Default

| Field    | Value              |
|----------|--------------------|
| Email    | admin@admin.com    |
| Password | 12345678           |

## URL Penting

| URL                              | Keterangan          |
|----------------------------------|---------------------|
| `http://localhost:8000/`         | Landing page        |
| `http://localhost:8000/auth/login` | Login             |
| `http://localhost:8000/admin/v1/dashboard/` | Dashboard  |
| `http://localhost:8000/api/v1/auth/login/`  | API login  |

## Perintah Bantu

```bash
# Cek konvensi kode
DJANGO_SETTINGS_MODULE=config.settings.development .venv/bin/python manage.py check_conventions

# Sync permission dari route ke DB
DJANGO_SETTINGS_MODULE=config.settings.development .venv/bin/python manage.py sync_permissions

# Generate scaffold modul baru (contoh: product)
DJANGO_SETTINGS_MODULE=config.settings.development .venv/bin/python manage.py make_module product
```

## Menjalankan Test

```bash
DJANGO_SETTINGS_MODULE=config.settings.testing .venv/bin/pytest
```

Dengan coverage:

```bash
DJANGO_SETTINGS_MODULE=config.settings.testing .venv/bin/pytest --cov=apps --cov=core
```

## Struktur Direktori

```
DjangoAdmin/
├── apps/                   # Feature apps (access, authentication, dashboard, ...)
├── config/                 # Settings, URLs, WSGI/ASGI
│   └── settings/
│       ├── base.py
│       ├── development.py
│       ├── testing.py
│       └── production.py
├── core/                   # Shared infrastructure (errors, helpers, RBAC, middleware)
├── templates/              # Django templates (be/default + fe/default)
├── tests/                  # pytest tests (unit, integration, api, smoke, bdd)
├── static/                 # Static assets
├── storage/                # Media uploads
├── .env.development        # Dev environment config
├── manage.py
└── requirements.txt
```

## Tema

Tersedia 9 tema (Blue default): Blue, Black, Brown, Green, Grey, Orange, Purple, Red, Yellow.
Ganti tema di `/admin/v1/setting/`.
