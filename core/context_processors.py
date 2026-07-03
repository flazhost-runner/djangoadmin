"""Template context processors — inject theme and setting into every template."""
import time
import threading
from django.conf import settings

_setting_cache = None
_setting_cache_time = 0.0
_setting_cache_ttl = 60
_setting_cache_lock = threading.Lock()


def _get_cached_setting():
    global _setting_cache, _setting_cache_time
    now = time.time()
    with _setting_cache_lock:
        if _setting_cache is None or (now - _setting_cache_time) > _setting_cache_ttl:
            try:
                from apps.setting.models import Setting
                _setting_cache = Setting.objects.first()
                _setting_cache_time = now
            except Exception:
                _setting_cache = None
        return _setting_cache


def theme_context(request):
    """Inject current theme palette as CSS vars."""
    try:
        s = _get_cached_setting()
        theme_name = s.theme if s and s.theme else 'Blue'
    except Exception:
        theme_name = 'Blue'

    themes = getattr(settings, 'THEMES', {})
    theme = themes.get(theme_name, themes.get('Blue', {}))
    return {
        'theme': theme,
        'themeName': theme_name,
        'themes': themes,
    }


def setting_context(request):
    """Inject Setting record into every template (cached 60s)."""
    return {'setting': _get_cached_setting()}
