from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from core.response import ResponseHandler
from core.errors import AppError
from apps.authentication.services.auth_service import AuthService


class ApiLoginView(APIView):
    def post(self, request):
        try:
            result = AuthService().login(
                request.data.get('email', ''),
                request.data.get('password', ''),
            )
            return ResponseHandler.success({
                'token': result['token'],
                'user': {'id': result['user'].id, 'email': result['user'].email},
            }, 'Login successful')
        except AppError as e:
            return ResponseHandler.error(e.message, e.status)


class ApiLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        token = request.auth
        if token:
            AuthService().logout(token)
        return ResponseHandler.success(None, 'Logged out successfully')


class ApiMeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = AuthService().me(request.user)
        return ResponseHandler.success(data)


class ApiRegisterView(APIView):
    def post(self, request):
        try:
            result = AuthService().register(dict(request.data))
            return ResponseHandler.success({'token': result['token']}, 'Registered successfully', 201)
        except AppError as e:
            return ResponseHandler.error(e.message, e.status)


class ApiResetRequestView(APIView):
    def post(self, request):
        try:
            AuthService().request_reset(request.data.get('email', ''))
            return ResponseHandler.success(None, 'OTP sent')
        except AppError as e:
            return ResponseHandler.error(e.message, e.status)


class ApiResetProcessView(APIView):
    def post(self, request):
        try:
            AuthService().process_reset(
                request.data.get('email', ''),
                request.data.get('otp', ''),
                request.data.get('new_password', ''),
            )
            return ResponseHandler.success(None, 'Password reset successful')
        except AppError as e:
            return ResponseHandler.error(e.message, e.status)
