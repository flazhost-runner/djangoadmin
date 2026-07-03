"""Shared helpers — paginate, ci_like, remove_empty_fields, etc."""
import math
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse


def remove_empty_fields(data: dict) -> dict:
    return {k: v for k, v in data.items() if v is not None and v != '' and v != []}


def ci_like(queryset, field, value):
    """Case-insensitive LIKE filter (works on MySQL/PG/SQLite via __icontains)."""
    return queryset.filter(**{f'{field}__icontains': value})


def paginate(queryset, params: dict) -> dict:
    """Returns {datas, paginate_data} matching NodeAdmin's paginate() shape."""
    page = max(1, int(params.get('q_page', 1) or 1))
    page_size = int(params.get('q_page_size', 10) or 10)
    total = queryset.count()
    total_page = max(1, math.ceil(total / page_size))
    page = min(page, total_page)
    offset = (page - 1) * page_size
    datas = list(queryset[offset:offset + page_size])

    # windowed pages (show 5 around current)
    window = 2
    start = max(1, page - window)
    end = min(total_page, page + window)
    pages = list(range(start, end + 1))

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


def add_or_update_query_param(url: str, key: str, value) -> str:
    """Add or update a query param in a URL string."""
    parsed = urlparse(url)
    params = parse_qs(parsed.query, keep_blank_values=True)
    params[key] = [str(value)]
    new_query = urlencode({k: v[0] for k, v in params.items()})
    return urlunparse(parsed._replace(query=new_query))


def get_timezones():
    import zoneinfo
    try:
        return sorted(zoneinfo.available_timezones())
    except Exception:
        return ['UTC', 'Asia/Jakarta', 'America/New_York', 'Europe/London']
