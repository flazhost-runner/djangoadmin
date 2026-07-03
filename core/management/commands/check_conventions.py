"""Convention checker — mirrors NodeAdmin's npm run lint:conventions."""
from django.core.management.base import BaseCommand
import os
import re
import sys


class Command(BaseCommand):
    help = 'Check DjangoAdmin conventions (services have ABC, views use RoutePermissionMixin, etc.)'

    def handle(self, *args, **options):
        errors = []
        base = os.path.join(os.getcwd(), 'apps')

        # Apps whose web views are intentionally public (login, landing, etc.)
        PUBLIC_APPS = {'authentication', 'home'}

        for app_dir in os.listdir(base):
            app_path = os.path.join(base, app_dir)
            if not os.path.isdir(app_path):
                continue
            services_path = os.path.join(app_path, 'services')
            if os.path.isdir(services_path):
                for fname in os.listdir(services_path):
                    if not fname.endswith('.py') or fname.startswith('i_') or fname == '__init__.py':
                        continue
                    fpath = os.path.join(services_path, fname)
                    content = open(fpath).read()
                    if 'class ' in content and '(IBase' not in content and 'ABC' not in content:
                        # Check if it implements an interface
                        has_interface = bool(re.search(r'class \w+\([^)]*[Ii][^)]*Service\)', content))
                        if not has_interface and 'ABC' not in content and 'Service' in fname:
                            errors.append(f'[convention] {fpath}: service does not implement interface (ABC)')

            views_path = os.path.join(app_path, 'views')
            if os.path.isdir(views_path) and app_dir not in PUBLIC_APPS:
                for root, dirs, files in os.walk(views_path):
                    for fname in files:
                        if not fname.endswith('.py') or fname == '__init__.py':
                            continue
                        # API views don't need session-based auth mixin
                        if 'api' in root.split(os.sep):
                            continue
                        fpath = os.path.join(root, fname)
                        content = open(fpath).read()
                        if 'class ' in content and 'View' in content:
                            if 'RoutePermissionMixin' not in content and 'LoginRequiredMixin' not in content and 'APIView' not in content:
                                if 'def get(' in content or 'def post(' in content:
                                    errors.append(f'[convention] {fpath}: web view missing RoutePermissionMixin or LoginRequiredMixin')

        if errors:
            for e in errors:
                self.stderr.write(self.style.ERROR(e))
            sys.exit(1)
        else:
            self.stdout.write(self.style.SUCCESS('All conventions pass!'))
