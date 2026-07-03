from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from core.permissions import HasRoutePermission
from core.response import ResponseHandler
from core.errors import AppError
from apps.access.services.permission_service import PermissionService

class PermissionApiIndex(APIView):
    permission_classes = [IsAuthenticated, HasRoutePermission]
    def get(self, request):
        try:
            result = PermissionService().index(request.GET.dict())
            datas = [{'id': str(p.id), 'name': p.name, 'method': p.method}
                     for p in result['datas']]
            return ResponseHandler.success({'datas': datas, **result['paginate_data']})
        except AppError as e:
            return ResponseHandler.error(e.message, e.status)
