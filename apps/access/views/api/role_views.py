from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from core.permissions import HasRoutePermission
from core.response import ResponseHandler
from core.errors import AppError
from apps.access.services.role_service import RoleService

class RoleApiIndex(APIView):
    permission_classes = [IsAuthenticated, HasRoutePermission]
    def get(self, request):
        try:
            result = RoleService().index(request.GET.dict())
            datas = [{'id': str(r.id), 'name': r.name, 'status': r.status}
                     for r in result['datas']]
            return ResponseHandler.success({'datas': datas, **result['paginate_data']})
        except AppError as e:
            return ResponseHandler.error(e.message, e.status)
