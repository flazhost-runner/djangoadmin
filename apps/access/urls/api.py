from django.urls import path
from apps.access.views.api.user_views import (
    UserApiIndex, UserApiStore, UserApiEdit, UserApiUpdate, UserApiDelete, UserApiDeleteSelected,
)
from apps.access.views.api.role_views import RoleApiIndex
from apps.access.views.api.permission_views import PermissionApiIndex

urlpatterns = [
    path('access/user', UserApiIndex.as_view(), name='api.v1.access.user.index'),
    path('access/user/store', UserApiStore.as_view(), name='api.v1.access.user.store'),
    path('access/user/<str:id>', UserApiEdit.as_view(), name='api.v1.access.user.edit'),
    path('access/user/<str:id>/update', UserApiUpdate.as_view(), name='api.v1.access.user.update'),
    path('access/user/<str:id>/delete', UserApiDelete.as_view(), name='api.v1.access.user.delete'),
    path('access/user/delete_selected', UserApiDeleteSelected.as_view(), name='api.v1.access.user.delete_selected'),
    path('access/role', RoleApiIndex.as_view(), name='api.v1.access.role.index'),
    path('access/permission', PermissionApiIndex.as_view(), name='api.v1.access.permission.index'),
]
