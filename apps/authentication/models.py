import uuid
from django.db import models


def _uuid4_str():
    return str(uuid.uuid4())


class BlacklistedToken(models.Model):
    class Meta:
        db_table = 'blacklisted_tokens'

    id = models.CharField(max_length=36, primary_key=True, default=_uuid4_str, editable=False)
    token = models.TextField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token[:30]
