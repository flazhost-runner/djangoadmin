from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from core.permissions import RoutePermissionMixin
from core.errors import AppError
from core.fe_templates import DEFAULT_FE_TEMPLATE
from apps.setting.services.setting_service import SettingService
from apps.home.services.fe_catalog_service import FeCatalogService


class SettingIndexView(RoutePermissionMixin, View):
    def get(self, request):
        data = SettingService().get()
        from django.conf import settings

        # FE catalog: server-side pagination + filter (q_name/q_category/
        # q_page). The active template is pinned to the first page.
        fe_catalog = FeCatalogService()
        active_slug = (getattr(data, 'fe_template', '') or '') or DEFAULT_FE_TEMPLATE
        result = fe_catalog.paginate(request.GET, pin_slug=active_slug)

        return render(request, 'be/default/setting/index.html', {
            'data': data,
            'themes': settings.THEMES,
            'fe_templates': result['datas'],
            'fe_categories': fe_catalog.categories(),
            'fe_active': active_slug,
            'paginate_data': result['paginate_data'],
            'filter': request.GET.dict(),
            'full_url': request.get_full_path(),
        })


class SettingUpdateView(RoutePermissionMixin, View):
    def put(self, request):
        try:
            data = dict(request.POST)
            data = {k: v[0] if isinstance(v, list) and len(v) == 1 else v for k, v in data.items()}
            data.pop('csrfmiddlewaretoken', None)
            SettingService().update(data, files=request.FILES, actor_id=request.user.id)
            messages.success(request, 'Save Setting Success.')
        except AppError as e:
            messages.error(request, e.message)
        return redirect('admin.v1.setting.index')


class SettingFePreviewView(RoutePermissionMixin, View):
    """Raw HTML preview of one FE template (thumbnail/modal; cached client-side)."""

    def get(self, request, slug):
        try:
            html = FeCatalogService().preview_html(slug)
        except AppError as e:
            return HttpResponse(e.message, status=e.status, content_type='text/plain; charset=utf-8')
        return HttpResponse(html, content_type='text/html; charset=utf-8')
