from django.urls import path
from apps.home.views.web_views import HomeView
urlpatterns = [
    path('', HomeView.as_view(), name='web.home.root'),
    path('home', HomeView.as_view(), name='web.home.index'),
]
