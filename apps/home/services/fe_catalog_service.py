"""FeCatalogService — frontend template catalog (640 opentailwind landings).
Mirrors NodeAdmin's home/http/services/v1/FeCatalogService.ts.

Source of truth = GitHub tree API, fetched ONCE then cached (process memory +
disk file) to avoid hammering GitHub. Search & pagination are server-side."""
import json
import math
import os
import threading
import time
import urllib.request

from django.conf import settings as django_settings

from core.errors import AppError
from core.fe_templates import (
    FE_TEMPLATE_BASE_URL,
    FE_TEMPLATE_TREE_URL,
    FE_TEMPLATE_CATALOG_FILE,
    FE_TEMPLATE_DIR,
    FE_TEMPLATES,
    derive_fe_template,
)

# In-memory catalog cache TTL (seconds). Disk persists across restarts.
CATALOG_TTL_SECONDS = 6 * 60 * 60  # 6 jam

# Timeout fetching one preview HTML file (seconds) — tight, single light file.
FETCH_TIMEOUT_SECONDS = 8

# Timeout fetching the catalog tree (seconds) — looser than preview: the
# recursive tree response covers 640 entries and only runs ONCE before being
# cached (memory + disk). Loose so a network blip does not degrade to the
# curated fallback (15 items) that makes the catalog look nearly empty.
TREE_FETCH_TIMEOUT_SECONDS = 20

_memo = {'at': 0.0, 'data': None}
_memo_lock = threading.Lock()


class FeCatalogService:
    def _cache_file(self) -> str:
        return os.path.join(django_settings.BASE_DIR, FE_TEMPLATE_CATALOG_FILE)

    def _local_html_file(self, slug: str) -> str:
        """Path of a locally downloaded template HTML (used as preview fallback)."""
        return os.path.join(django_settings.BASE_DIR, FE_TEMPLATE_DIR, f'{slug}.html')

    def _fetch(self, url: str, timeout: int = FETCH_TIMEOUT_SECONDS, headers: dict = None) -> str:
        req_headers = {'User-Agent': 'DjangoAdmin/1.0'}
        if headers:
            req_headers.update(headers)
        req = urllib.request.Request(url, headers=req_headers)
        with urllib.request.urlopen(req, timeout=timeout) as res:
            if res.status != 200:
                raise AppError(f'HTTP {res.status}', 502)
            return res.read().decode('utf-8', errors='replace')

    def _parse_tree(self, tree: list) -> list:
        """Parse tree paths -> landing slugs (strip `landings/` prefix & `.html`)."""
        items = [
            derive_fe_template(node['path'][len('landings/'):-len('.html')])
            for node in tree
            if isinstance(node, dict)
            and node.get('type') == 'blob'
            and isinstance(node.get('path'), str)
            and node['path'].startswith('landings/')
            and node['path'].endswith('.html')
        ]
        # Stable order: category then name.
        items.sort(key=lambda t: (t['category'], t['name']))
        return items

    def _read_disk_cache(self):
        try:
            with open(self._cache_file(), 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data if isinstance(data, list) and len(data) > 0 else None
        except Exception:
            return None

    def _write_disk_cache(self, data: list) -> None:
        try:
            os.makedirs(os.path.dirname(self._cache_file()), exist_ok=True)
            with open(self._cache_file(), 'w', encoding='utf-8') as f:
                json.dump(data, f)
        except Exception:
            pass  # best-effort disk cache — write failure must not break list().

    def list(self) -> list:
        with _memo_lock:
            if _memo['data'] is not None and time.time() - _memo['at'] < CATALOG_TTL_SECONDS:
                return _memo['data']

        disk = self._read_disk_cache()
        if disk:
            with _memo_lock:
                _memo['at'], _memo['data'] = time.time(), disk
            return disk

        # No cache yet → fetch the GitHub tree once.
        try:
            raw = self._fetch(
                FE_TEMPLATE_TREE_URL,
                timeout=TREE_FETCH_TIMEOUT_SECONDS,
                headers={'Accept': 'application/vnd.github+json'},
            )
            body = json.loads(raw)
            data = self._parse_tree(body.get('tree') or [])
            if not data:
                raise AppError('katalog kosong', 502)
            with _memo_lock:
                _memo['at'], _memo['data'] = time.time(), data
            self._write_disk_cache(data)
            return data
        except Exception as e:
            # Fallback to the curated catalog so the UI keeps working offline.
            import logging
            logging.getLogger(__name__).error(
                'Fetch katalog opentailwind gagal, pakai fallback kurasi: %s', e)
            fallback = [dict(t) for t in FE_TEMPLATES]
            with _memo_lock:
                _memo['at'], _memo['data'] = time.time(), fallback
            return fallback

    def categories(self) -> list:
        return sorted({t['category'] for t in self.list()})

    def paginate(self, params: dict, pin_slug: str = None) -> dict:
        """Server-side filter (q_name / q_category) + pagination (q_page /
        q_page_size). pin_slug pins the active template to page 1. Returns
        {datas, paginate_data} matching core.helpers.paginate() shape."""
        q_name = str(params.get('q_name') or '').strip().lower()
        q_category = str(params.get('q_category') or '').strip()

        filtered = [
            t for t in self.list()
            if (not q_name or q_name in t['name'].lower() or q_name in t['slug'].lower())
            and (not q_category or t['category'] == q_category)
        ]

        # Pin the active template to the front (when it passes the filter) so
        # the admin sees the current choice on the first page.
        if pin_slug:
            for i, t in enumerate(filtered):
                if t['slug'] == pin_slug:
                    if i > 0:
                        filtered.insert(0, filtered.pop(i))
                    break

        try:
            page_size = int(params.get('q_page_size') or 12)
        except (TypeError, ValueError):
            page_size = 12
        page_size = page_size if page_size > 0 else 12
        try:
            page = int(params.get('q_page') or 1)
        except (TypeError, ValueError):
            page = 1
        page = page if page > 0 else 1

        total = len(filtered)
        total_page = max(1, math.ceil(total / page_size))
        page = min(page, total_page)
        offset = (page - 1) * page_size
        datas = filtered[offset:offset + page_size]

        window = 2
        pages = list(range(max(1, page - window), min(total_page, page + window) + 1))

        return {
            'datas': datas,
            'paginate_data': {
                'current_page': page,
                'total_page': total_page,
                'page_size': page_size,
                'total': total,
                'pages': pages,
                'offset': offset,
            },
        }

    def has(self, slug: str) -> bool:
        """True when the slug exists in the catalog (anti-SSRF whitelist)."""
        return any(t['slug'] == slug for t in self.list())

    def _read_local_html(self, slug: str):
        """Read template HTML from the local cache when present & valid."""
        try:
            with open(self._local_html_file(slug), 'r', encoding='utf-8') as f:
                html = f.read()
            return html if '</html>' in html.lower() else None
        except Exception:
            return None

    def preview_html(self, slug: str) -> str:
        """Raw HTML of one template (for thumbnails/preview modal)."""
        if not self.has(slug):
            raise AppError('Template tidak dikenali', 400)

        # 1) Local cache first — instant, no network/rate-limit dependency.
        local = self._read_local_html(slug)
        if local:
            return local

        # 2) Fetch upstream with a timeout so slow GitHub does not hang us.
        url = f'{FE_TEMPLATE_BASE_URL}/{slug}.html'
        try:
            html = self._fetch(url)
            if '</html>' not in html.lower():
                raise AppError('HTML tidak valid', 502)
            return html
        except Exception as e:
            # 3) Last fallback: local cache (in case it appeared meanwhile).
            fallback = self._read_local_html(slug)
            if fallback:
                return fallback
            reason = e.message if isinstance(e, AppError) else str(e)
            raise AppError(f'Gagal mengambil preview: {reason}', 502)
