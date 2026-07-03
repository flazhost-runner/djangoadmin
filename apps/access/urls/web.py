from django.urls import path
from apps.access.views.web.user_views import (
    UserIndexView, UserCreateView, UserStoreView,
    UserEditView, UserUpdateView, UserDeleteView, UserDeleteSelectedView,
)
from apps.access.views.web.role_views import (
    RoleIndexView, RoleCreateView, RoleStoreView,
    RoleEditView, RoleUpdateView, RoleDeleteView, RoleDeleteSelectedView,
    RolePermissionView, RolePermissionAssignView, RolePermissionUnassignView,
    RolePermissionAssignSelectedView, RolePermissionUnassignSelectedView,
)
from apps.access.views.web.permission_views import (
    PermissionIndexView, PermissionCreateView, PermissionStoreView,
    PermissionEditView, PermissionUpdateView, PermissionDeleteView,
    PermissionDeleteSelectedView, PermissionSyncView,
)

urlpatterns = [
    # Users
    path('access/user', UserIndexView.as_view(), name='admin.v1.access.user.index'),
    path('access/user/create', UserCreateView.as_view(), name='admin.v1.access.user.create'),
    path('access/user/store', UserStoreView.as_view(), name='admin.v1.access.user.store'),
    path('access/user/<str:id>/edit', UserEditView.as_view(), name='admin.v1.access.user.edit'),
    path('access/user/<str:id>/update', UserUpdateView.as_view(), name='admin.v1.access.user.update'),
    path('access/user/<str:id>/delete', UserDeleteView.as_view(), name='admin.v1.access.user.delete'),
    path('access/user/delete_selected', UserDeleteSelectedView.as_view(), name='admin.v1.access.user.delete_selected'),
    # Roles
    path('access/role', RoleIndexView.as_view(), name='admin.v1.access.role.index'),
    path('access/role/create', RoleCreateView.as_view(), name='admin.v1.access.role.create'),
    path('access/role/store', RoleStoreView.as_view(), name='admin.v1.access.role.store'),
    path('access/role/<str:id>/edit', RoleEditView.as_view(), name='admin.v1.access.role.edit'),
    path('access/role/<str:id>/update', RoleUpdateView.as_view(), name='admin.v1.access.role.update'),
    path('access/role/<str:id>/delete', RoleDeleteView.as_view(), name='admin.v1.access.role.delete'),
    path('access/role/delete_selected', RoleDeleteSelectedView.as_view(), name='admin.v1.access.role.delete_selected'),
    path('access/role/<str:id>/permission', RolePermissionView.as_view(), name='admin.v1.access.role.permission'),
    path('access/role/<str:id>/permission/<str:perm_id>/assign', RolePermissionAssignView.as_view(), name='admin.v1.access.role.permission.assign'),
    path('access/role/<str:id>/permission/<str:perm_id>/unassign', RolePermissionUnassignView.as_view(), name='admin.v1.access.role.permission.unassign'),
    path('access/role/<str:id>/permission/assign_selected', RolePermissionAssignSelectedView.as_view(), name='admin.v1.access.role.permission.assign_selected'),
    path('access/role/<str:id>/permission/unassign_selected', RolePermissionUnassignSelectedView.as_view(), name='admin.v1.access.role.permission.unassign_selected'),
    # Permissions
    path('access/permission', PermissionIndexView.as_view(), name='admin.v1.access.permission.index'),
    path('access/permission/create', PermissionCreateView.as_view(), name='admin.v1.access.permission.create'),
    path('access/permission/store', PermissionStoreView.as_view(), name='admin.v1.access.permission.store'),
    path('access/permission/<str:id>/edit', PermissionEditView.as_view(), name='admin.v1.access.permission.edit'),
    path('access/permission/<str:id>/update', PermissionUpdateView.as_view(), name='admin.v1.access.permission.update'),
    path('access/permission/<str:id>/delete', PermissionDeleteView.as_view(), name='admin.v1.access.permission.delete'),
    path('access/permission/delete_selected', PermissionDeleteSelectedView.as_view(), name='admin.v1.access.permission.delete_selected'),
    path('access/permission/sync', PermissionSyncView.as_view(), name='admin.v1.access.permission.sync'),
]
