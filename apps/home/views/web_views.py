from django.http import HttpResponse
from django.views import View
from django.shortcuts import render


class HomeView(View):
    """Public landing page (frontend).

    - Active slug 'default' → render the local Django landing view
      (fe/default, landing v6 — header/footer partials + assets under
      static/fe/default, mirroring NodeAdmin's EJS fe/default layout).
    - Any other slug → serve the cached self-contained opentailwind HTML raw
      (downloaded on-demand & cached under storage/fe/templates). When no
      HTML is available (offline, download failed) → fall back to the local
      default landing so the page always renders.
    """

    def get(self, request):
        from apps.home.services.fe_template_service import FeTemplateService
        from apps.home.services.home_service import HomeService

        fe_template = FeTemplateService()
        slug = fe_template.get_active_slug()
        if not fe_template.is_default_view(slug):
            html = fe_template.get_active_html()
            if html is not None:
                return HttpResponse(html, content_type='text/html; charset=utf-8')

        data = HomeService().get_landing_data()
        return render(request, 'fe/default/home/index.html', data)
