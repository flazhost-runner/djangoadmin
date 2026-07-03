from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from core.permissions import RoutePermissionMixin
from core.errors import AppError
from apps.setting.services.setting_service import SettingService
from apps.setting.services.fe_catalog_service import FeCatalogService


class SettingIndexView(RoutePermissionMixin, View):
    def get(self, request):
        data = SettingService().get()
        from django.conf import settings

        fe_svc = FeCatalogService()
        q_name = request.GET.get('q_name', '')
        q_category = request.GET.get('q_category', '')
        fe_page = int(request.GET.get('fe_page', 1))
        active_slug = getattr(data, 'fe_template', '') or 'agency-consulting-002-creative-agency'
        catalog = fe_svc.get_catalog(
            search=q_name, category=q_category, page=fe_page, active_slug=active_slug
        )
        fe_categories = fe_svc.get_categories()

        return render(request, 'be/default/setting/index.html', {
            'data': data,
            'themes': settings.THEMES,
            'fe_templates': catalog['items'],
            'fe_active': active_slug,
            'fe_search': q_name,
            'fe_category': q_category,
            'fe_categories': fe_categories,
            'paginate_data': catalog,
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
