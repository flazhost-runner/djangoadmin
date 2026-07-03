"""Django RBAC permissions — route-driven, mirrors NodeAdmin's AccessMiddleware."""
from rest_framework.permissions import BasePermission
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from core.errors import ForbiddenError


def _check_route_access(user, url_name: str, method: str) -> bool:
    """Returns True if user has access to this named route + method."""
    if not user or not user.is_authenticated:
        return False
    if user.is_administrator():
        return True
    from apps.access.models import UsersRoles
    return UsersRoles.objects.filter(
        user=user,
        role__roles_permissions__permission__name=url_name,
        role__roles_permissions__permission__method=method.upper(),
    ).exists()


class HasRoutePermission(BasePermission):
    """DRF permission class — route-driven RBAC for API views."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        url_name = getattr(request.resolver_match, 'url_name', None)
        if not url_name:
            return True
        return _check_route_access(request.user, url_name, request.method)


class RoutePermissionMixin(LoginRequiredMixin):
    """Django view mixin — route-driven RBAC for web views.
    Unauthenticated → redirect to login. Forbidden → flash 'Unauthorized.' + redirect Referrer."""
    login_url = '/auth/login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url)
        url_name = getattr(request.resolver_match, 'url_name', None)
        if url_name and not _check_route_access(request.user, url_name, request.method):
            from django.contrib import messages as django_messages
            django_messages.error(request, 'Unauthorized.')
            referrer = request.META.get('HTTP_REFERER', '/')
            return redirect(referrer)
        return super().dispatch(request, *args, **kwargs)
