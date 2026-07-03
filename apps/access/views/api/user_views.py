from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from core.permissions import HasRoutePermission
from core.response import ResponseHandler
from core.errors import AppError
from apps.access.services.user_service import UserService

class UserApiIndex(APIView):
    permission_classes = [IsAuthenticated, HasRoutePermission]
    def get(self, request):
        try:
            result = UserService().index(request.GET.dict())
            datas = [{'id': str(u.id), 'email': u.email, 'name': u.name, 'status': u.status}
                     for u in result['datas']]
            return ResponseHandler.success({'datas': datas, **result['paginate_data']})
        except AppError as e:
            return ResponseHandler.error(e.message, e.status)

class UserApiStore(APIView):
    permission_classes = [IsAuthenticated, HasRoutePermission]
    def post(self, request):
        try:
            data = request.data.copy() if hasattr(request.data, 'copy') else dict(request.data)
            data['roles'] = request.data.getlist('roles[]') if hasattr(request.data, 'getlist') else data.pop('roles', [])
            user = UserService().store(data, actor_id=request.user.id)
            return ResponseHandler.success({'id': user.id, 'email': user.email}, 'Store User Success', 201)
        except AppError as e:
            return ResponseHandler.error(e.message, e.status)

class UserApiEdit(APIView):
    permission_classes = [IsAuthenticated, HasRoutePermission]
    def get(self, request, id):
        try:
            user = UserService().edit(id)
            return ResponseHandler.success({'id': user.id, 'email': user.email, 'name': user.name})
        except AppError as e:
            return ResponseHandler.error(e.message, e.status)

class UserApiUpdate(APIView):
    permission_classes = [IsAuthenticated, HasRoutePermission]
    def put(self, request, id):
        try:
            data = dict(request.data)
            UserService().update(id, data, actor_id=request.user.id)
            return ResponseHandler.success(None, 'Update User Success')
        except AppError as e:
            return ResponseHandler.error(e.message, e.status)

class UserApiDelete(APIView):
    permission_classes = [IsAuthenticated, HasRoutePermission]
    def delete(self, request, id):
        try:
            UserService().delete(id)
            return ResponseHandler.success(None, 'Delete User Success')
        except AppError as e:
            return ResponseHandler.error(e.message, e.status)

class UserApiDeleteSelected(APIView):
    permission_classes = [IsAuthenticated, HasRoutePermission]
    def delete(self, request):
        ids = request.data.get('selected', [])
        count = UserService().delete_selected(ids)
        return ResponseHandler.success({'count': count}, 'Delete Selected Success')
