# Architecture — DjangoAdmin

Django 6 + DRF 3.17 port of NodeAdmin. Native Django idioms.

## Stack
- Django 6.0.6 + DRF 3.17.1
- SQLite (dev/test) / MySQL / PostgreSQL (prod)
- PyJWT for API authentication
- django-environ for env config
- Tailwind CSS (CDN) + Font Awesome

## Request Lifecycle
Request → WSGI → Middleware (Method Override → CSRF → Auth) → URLconf → View → Service → ORM → Response

## RBAC (Route-Driven)
Mirrors NodeAdmin exactly:
- Permission.name = Django URL name (e.g. 'admin.v1.access.user.index')
- Permission.method = HTTP method (GET/POST/PUT/DELETE)
- Administrator role bypasses all checks
- Web: RoutePermissionMixin, API: HasRoutePermission
- Sync: python manage.py sync_permissions

## Layers
| Layer | Location |
|-------|----------|
| URL | apps/*/urls/*.py |
| View | apps/*/views/*.py |
| Service | apps/*/services/*.py |
| Model | apps/*/models.py |
| Template | templates/be/default/ |

## Canonical DB Schema
Byte-identical to NodeAdmin (see PORTING_GUIDE.md in NodeAdmin reference).
