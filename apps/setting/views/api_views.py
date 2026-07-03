from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from core.permissions import HasRoutePermission
from core.response import ResponseHandler
from core.errors import AppError
from apps.setting.services.setting_service import SettingService


class ApiSettingIndex(APIView):
    permission_classes = [IsAuthenticated, HasRoutePermission]
    def get(self, request):
        s = SettingService().get()
        return ResponseHandler.success({'name': s.name if s else None, 'theme': s.theme if s else 'Blue'})


class ApiSettingUpdate(APIView):
    permission_classes = [IsAuthenticated, HasRoutePermission]
    def put(self, request):
        try:
            s = SettingService().update(dict(request.data), actor_id=request.user.id)
            return ResponseHandler.success({'theme': s.theme}, 'Setting updated')
        except AppError as e:
            return ResponseHandler.error(e.message, e.status)
