from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from core.response import ResponseHandler
from core.errors import AppError
from apps.profile.services.profile_service import ProfileService

class ProfileApiIndex(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user = ProfileService().get(request.user.id)
            return ResponseHandler.success({
                'id': str(user.id),
                'email': user.email,
                'name': user.name,
                'phone': user.phone,
                'status': user.status,
            })
        except AppError as e:
            return ResponseHandler.error(e.message, e.status)
