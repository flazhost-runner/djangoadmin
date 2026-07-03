"""ResponseHandler — matches NodeAdmin's {status, message, data} contract."""
from rest_framework.response import Response


class ResponseHandler:
    @staticmethod
    def success(data=None, message='Success', status=200):
        return Response({'status': True, 'message': message, 'data': data}, status=status)

    @staticmethod
    def error(message='Error', status=400, errors=None):
        payload = {'status': False, 'message': message, 'data': None}
        if errors:
            payload['errors'] = errors
        return Response(payload, status=status)
