import json
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.media.services.media_service import MediaService
from core.errors import AppError

_MAX_UPLOAD_BYTES = 2 * 1024 * 1024
_ALLOWED_MIME = {'image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/gif'}


class MediaListView(LoginRequiredMixin, View):
    def get(self, request):
        files = MediaService().list_files()
        return JsonResponse({'status': True, 'message': 'Success', 'data': files})


class MediaUploadView(LoginRequiredMixin, View):
    def post(self, request):
        f = request.FILES.get('file')
        if not f:
            return JsonResponse({'status': False, 'message': 'No file provided', 'data': None}, status=400)
        if f.size > _MAX_UPLOAD_BYTES:
            return JsonResponse({'status': False, 'message': 'File too large. Max 2MB.', 'data': None}, status=400)
        if f.content_type not in _ALLOWED_MIME and not f.content_type.startswith('image/'):
            return JsonResponse({'status': False, 'message': 'Invalid file type.', 'data': None}, status=400)
        try:
            result = MediaService().upload(f)
            return JsonResponse({'status': True, 'message': 'Upload Success.', 'data': result})
        except AppError as e:
            return JsonResponse({'status': False, 'message': e.message, 'data': None}, status=e.status)


class MediaDeleteView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            body = json.loads(request.body)
            key = body.get('key', '')
        except (json.JSONDecodeError, AttributeError):
            key = request.POST.get('key', '')
        if not key:
            return JsonResponse({'status': False, 'message': 'Key required', 'data': None}, status=400)
        try:
            MediaService().delete_file(key)
            return JsonResponse({'status': True, 'message': 'Delete Success.', 'data': None})
        except AppError as e:
            return JsonResponse({'status': False, 'message': e.message, 'data': None}, status=e.status)
