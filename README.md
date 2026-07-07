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

## Storage & switching backends

Upload gambar (logo/favicon/login image di Setting, dan editor media) melewati
satu abstraksi storage yang dipilih lewat env `STORAGE_DRIVER`. **Berpindah
backend cukup ubah `.env` lalu restart — tanpa edit kode atau template.**

| Driver         | `STORAGE_DRIVER` | Render URL gambar                                   | Butuh kredensial   |
|----------------|------------------|-----------------------------------------------------|--------------------|
| Lokal (default)| `local`          | Relatif, `MEDIA_URL` + key → `/media/<key>`         | Tidak              |
| Alibaba OSS    | `oss`            | Absolut (presigned/public) dari bucket OSS          | Ya (`STORAGE_*`)   |
| AWS S3 / kompatibel (MinIO, R2, B2) | `s3` | Absolut (presigned/public) dari bucket S3        | Ya (`STORAGE_*`)   |

**Cara render (kontrak URL).** Template tidak pernah hard-code `/media/...`.
Semua gambar dirender lewat template tag `{% get_file value %}` (lihat
`core/templatetags/core_tags.py`) yang bersifat *driver-agnostic* dan idempotent:

- Nilai berupa URL absolut (`http(s)://…`, mis. presigned OSS/S3) → dikembalikan apa adanya.
- Nilai berupa object key (`setting/uuid.png`) → diberi prefix `MEDIA_URL` → `/media/setting/uuid.png`.
- Nilai yang sudah absolut-path (`/media/…`) → dikembalikan apa adanya (mencegah dobel-prefix).

Jadi cukup nilai yang tersimpan berbeda per-driver; layer render tidak berubah
saat `STORAGE_DRIVER` diganti.

**Driver lokal disajikan di produksi juga.** File lokal dilayani dari aplikasi
di prefix `MEDIA_URL` (`/media/`) lewat route yang didaftarkan **tanpa syarat**
di `config/urls.py` (bukan lewat helper `static()` bawaan Django yang hanya
aktif saat `DEBUG=True`). Artinya gambar tetap tampil di `DEBUG=False`.

**Konfigurasi env** (lihat `.env.example`):

```env
STORAGE_DRIVER=local            # local | oss | s3
STORAGE_ACCESS_KEY_ID=
STORAGE_SECRET_ACCESS_KEY=
STORAGE_ENDPOINT=               # mis. oss-ap-southeast-5.aliyuncs.com / https://minio.local:9000
STORAGE_BUCKET=
STORAGE_REGION=                 # untuk S3 (mis. us-east-1)
STORAGE_SSL=true
```

Ganti driver → simpan `.env` → **restart** proses (gunicorn/uwsgi/runserver).
Tidak ada perubahan kode/template.

### Catatan operasional

- **DB menyimpan key/path objek, bukan blob.** Yang tersimpan di database hanya
  path/key file; byte gambar ada di storage backend. Karena itu berpindah
  backend **tidak** memindahkan file yang sudah ada.
- **Migrasi file antar backend.** Salin isi bucket/direktori secara terpisah
  saat berpindah, mis.:
  - OSS: `ossutil cp -r oss://<bucket>/ ./storage/` (atau sebaliknya)
  - S3:  `aws s3 sync s3://<bucket>/ ./storage/` (atau sebaliknya)
- **Lokal di produksi bersifat ephemeral.** `MEDIA_ROOT` = `storage/` di dalam
  repo. Di container/PaaS yang filesystem-nya sementara, mount **volume
  persisten** ke `storage/` (atau pindah ke `oss`/`s3`) agar upload tidak hilang
  saat redeploy. Untuk skala/throughput, letakkan nginx/CDN di depan `/media/`.
- **Upload di-git-ignore.** Isi `storage/` diabaikan git; direktori dijaga
  lewat `storage/.gitkeep` dan `storage/editor/.gitkeep`.

> Status port: driver `local` sudah aktif penuh (dev + prod). Kunci env
> `STORAGE_*` untuk `oss`/`s3` sudah disiapkan dan layer render sudah
> meneruskan URL absolut apa adanya; backend upload OSS/S3 (put/list/delete via
> SDK) menyusul mengikuti referensi NodeAdmin.

## API (Postman)

Koleksi Postman tersedia di `docs/postman/DjangoAdmin.postman_collection.json`.

Import ke Postman, lalu set variable `base_url` (default `http://localhost:8000`) dan `access_token` (dari `POST /api/v1/auth/login/`).

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
