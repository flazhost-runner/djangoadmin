from django.urls import path
from apps.components.views.web_views import ComponentsIndexView
urlpatterns = [
    path('components', ComponentsIndexView.as_view(), name='admin.v1.components.index'),
]
