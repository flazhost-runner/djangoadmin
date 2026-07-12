import os
import uuid
from django.conf import settings
from core.errors import AppError, ValidationError


ALLOWED_MIMES = {
    b'\xff\xd8\xff': 'image/jpeg',
    b'\x89PNG': 'image/png',
    b'GIF8': 'image/gif',
    b'RIFF': 'image/webp',
}
UPLOAD_DIR = 'editor'


class MediaService:
    def list_files(self) -> list:
        upload_path = os.path.join(settings.MEDIA_ROOT, UPLOAD_DIR)
        os.makedirs(upload_path, exist_ok=True)
        files = []
        for fname in os.listdir(upload_path):
            fpath = os.path.join(upload_path, fname)
            if os.path.isfile(fpath):
                files.append({
                    'name': fname,
                    'url': f'{settings.MEDIA_URL}{UPLOAD_DIR}/{fname}',
                    'size': os.path.getsize(fpath),
                })
        return files

    def upload(self, file) -> dict:
        header = file.read(4)
        file.seek(0)
        valid = any(header.startswith(sig) for sig in ALLOWED_MIMES)
        if not valid:
            raise ValidationError('Invalid file type. Only images allowed.')
        ext = os.path.splitext(file.name)[1].lower()
        fname = f'{uuid.uuid4()}{ext}'
        upload_path = os.path.join(settings.MEDIA_ROOT, UPLOAD_DIR)
        os.makedirs(upload_path, exist_ok=True)
        fpath = os.path.join(upload_path, fname)
        with open(fpath, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)
        return {
            'name': fname,
            'url': f'{settings.MEDIA_URL}{UPLOAD_DIR}/{fname}',
        }

    def delete_file(self, filename: str) -> None:
        safe_name = os.path.basename(filename)
        fpath = os.path.join(settings.MEDIA_ROOT, UPLOAD_DIR, safe_name)
        if not os.path.exists(fpath):
            from core.errors import NotFoundError
            raise NotFoundError('File not found')
        os.remove(fpath)
