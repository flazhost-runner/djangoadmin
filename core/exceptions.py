"""Custom DRF exception handler — maps AppError subclasses to HTTP responses."""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from core.errors import AppError


def custom_exception_handler(exc, context):
    if isinstance(exc, AppError):
        return Response({
            'success': False,
            'message': exc.message,
            'status': exc.status,
        }, status=exc.status)

    response = exception_handler(exc, context)
    if response is not None:
        return response

    return Response({
        'success': False,
        'message': 'Internal Server Error',
        'status': 500,
    }, status=500)
