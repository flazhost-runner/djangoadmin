from django.views import View
from django.shortcuts import render


class HomeView(View):
    def get(self, request):
        from apps.home.services.home_service import HomeService
        data = HomeService().get_landing_data()
        return render(request, 'fe/default/home/index.html', data)
