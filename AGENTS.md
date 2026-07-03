# AGENTS.md — DjangoAdmin Development Rules

## Arsitektur
DjangoAdmin = Django 6 + DRF 3.17 port of NodeAdmin. Native Django idioms.

## Request Lifecycle
Request → URLconf → View (RoutePermissionMixin) → Service → ORM → Response/Template

## Prinsip SOLID + DI
- Service: class implementing ABC interface (IXService)
- View: Django View / DRF APIView — injeksi service langsung
- RBAC: RoutePermissionMixin (web) + HasRoutePermission (API)
- Error: service throw AppError; dilarang return error

## Entity Rules (canonical schema)
- id = CharField(max_length=36, primary_key=True, default=lambda: str(uuid.uuid4()))
- Tipe kolom portabel: CharField/TextField/BooleanField/BigIntegerField/DateTimeField
- Explicit db_table + db_column untuk kolom reserved word (desc)
- M2M via explicit through models (UsersRoles, RolesPermissions) dengan pinned column names

## Wajib sebelum commit
1. python manage.py check_conventions
2. .venv/bin/ruff check .
3. .venv/bin/mypy . --ignore-missing-imports
4. pytest (semua hijau)

## DO NOT
- Jangan pakai process.env / os.environ langsung di app code
- Jangan pakai return error — throw/raise AppError
- Jangan pakai auto-increment ID — selalu UUID CharField
- Jangan buat module baru tanpa test
