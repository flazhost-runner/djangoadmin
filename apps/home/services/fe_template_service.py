"""FeTemplateService — active frontend (landing) template resolution + on-demand
download/cache. Mirrors NodeAdmin's home/http/services/v1/FeTemplateService.ts."""
import os
import urllib.request
import urllib.error

from django.conf import settings as django_settings

from core.errors import AppError
from core.fe_templates import (
    FE_TEMPLATE_BASE_URL,
    FE_TEMPLATE_DIR,
    FE_TEMPLATE_SLUG_RE,
    FE_TEMPLATE_DEFAULT_VIEW,
    DEFAULT_FE_TEMPLATE,
)

# Timeout for downloading a single template HTML file (seconds).
FETCH_TIMEOUT_SECONDS = 15


class FeTemplateService:
    def _dir(self) -> str:
        return os.path.join(django_settings.BASE_DIR, FE_TEMPLATE_DIR)

    def _file(self, slug: str) -> str:
        return os.path.join(self._dir(), f'{slug}.html')

    def is_cached(self, slug: str) -> bool:
        return os.path.exists(self._file(slug))

    def is_valid_slug(self, slug: str) -> bool:
        """A slug is valid when it is the special 'default' (local Django view)
        or matches the opentailwind pattern `{category}-{NNN}-{name}` — covering
        all 640 landings without binding to the static curated catalog.
        (Anti-SSRF: the pattern restricts charset to a-z0-9- + fixed structure.)"""
        if not slug:
            return False
        return slug == FE_TEMPLATE_DEFAULT_VIEW or bool(FE_TEMPLATE_SLUG_RE.match(slug))

    def get_active_slug(self) -> str:
        """Active template slug from Setting (fallback to default)."""
        from apps.setting.models import Setting
        setting = Setting.objects.only('fe_template').first()
        slug = (setting.fe_template or '').strip() if setting else ''
        return slug if self.is_valid_slug(slug) else DEFAULT_FE_TEMPLATE

    def is_default_view(self, slug: str) -> bool:
        """True when the slug is 'default' — rendered via the local Django
        landing view (fe/default, landing v6), not raw cached HTML."""
        return slug == FE_TEMPLATE_DEFAULT_VIEW

    def ensure(self, slug: str) -> None:
        """Make sure the template exists locally. If not cached yet, download
        the HTML from opentailwind (GitHub raw) into the cache folder. Only
        slugs matching the opentailwind pattern are allowed (anti-SSRF)."""
        if not self.is_valid_slug(slug):
            raise AppError('Template tidak dikenali', 400)
        if slug == FE_TEMPLATE_DEFAULT_VIEW or self.is_cached(slug):
            return

        url = f'{FE_TEMPLATE_BASE_URL}/{slug}.html'
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'DjangoAdmin/1.0'})
            with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT_SECONDS) as res:
                if res.status != 200:
                    raise AppError(f'Gagal mengunduh template: HTTP {res.status}', 502)
                html = res.read().decode('utf-8', errors='replace')
        except AppError:
            raise
        except Exception as e:  # URLError, timeout, dsb.
            raise AppError(f'Gagal mengunduh template: {e}', 502)

        if '</html>' not in html.lower():
            raise AppError('Template terunduh tidak valid', 502)

        os.makedirs(self._dir(), exist_ok=True)
        with open(self._file(slug), 'w', encoding='utf-8') as f:
            f.write(html)

    def get_active_html(self):
        """Raw HTML of the active landing (None when the active template is the
        local 'default' view or no cached/downloadable HTML is available — the
        caller then renders the bundled fe/default landing as a safe fallback).
        Downloads on first use (best-effort) so a fresh install serves the
        default opentailwind template as soon as the network allows."""
        slug = self.get_active_slug()
        if self.is_default_view(slug):
            return None

        if not self.is_cached(slug):
            try:
                self.ensure(slug)
            except AppError:
                pass  # offline/failed download → fall through to fallback

        target = slug if self.is_cached(slug) else DEFAULT_FE_TEMPLATE
        file = self._file(target)
        if not os.path.exists(file):
            return None
        with open(file, 'r', encoding='utf-8') as f:
            return f.read()
