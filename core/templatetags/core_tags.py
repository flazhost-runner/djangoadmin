"""Custom template tags for DjangoAdmin."""
from django import template
from django.urls import reverse, NoReverseMatch

register = template.Library()


@register.simple_tag(takes_context=True)
def has_access(context, route_name, method='GET'):
    """Check if current user has RBAC access to a named route."""
    request = context.get('request')
    if not request or not request.user or not request.user.is_authenticated:
        return False
    try:
        if request.user.is_administrator():
            return True
        from apps.access.models import UsersRoles
        return UsersRoles.objects.filter(
            user=request.user,
            role__roles_permissions__permission__name=route_name,
            role__roles_permissions__permission__method=method.upper(),
        ).exists()
    except Exception:
        return False


@register.simple_tag(takes_context=True)
def has_role(context, role_name):
    """Check if current user has a specific role."""
    request = context.get('request')
    if not request or not request.user or not request.user.is_authenticated:
        return False
    try:
        return request.user.roles.filter(name=role_name).exists()
    except Exception:
        return False


@register.simple_tag
def get_file(file_name):
    """Return the URL for a stored file. Mirrors NodeAdmin's getFile() helper."""
    from django.conf import settings as django_settings
    if not file_name:
        return ''
    if file_name.startswith('http://') or file_name.startswith('https://'):
        return file_name
    base = django_settings.MEDIA_URL.rstrip('/')
    name = file_name.lstrip('/')
    return f'{base}/{name}'


@register.simple_tag
def add_or_update_param(url, key, value):
    """Add or update a query param in a URL."""
    from core.helpers import add_or_update_query_param
    return add_or_update_query_param(url, key, value)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def split(value, sep=','):
    return value.split(sep)


@register.simple_tag(takes_context=True)
def full_url(context):
    request = context.get('request')
    if request:
        return request.build_absolute_uri()
    return ''


@register.simple_tag(takes_context=True)
def current_url(context):
    request = context.get('request')
    if request:
        return request.get_full_path()
    return ''
