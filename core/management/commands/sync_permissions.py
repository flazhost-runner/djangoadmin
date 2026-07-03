"""Sync permissions from registered URL routes."""
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Sync permissions from all registered URL routes (idempotent upsert).'

    def handle(self, *args, **options):
        from apps.access.services.permission_service import PermissionService
        count = PermissionService().sync_from_routes()
        self.stdout.write(self.style.SUCCESS(f'Synced {count} new permissions from routes.'))
