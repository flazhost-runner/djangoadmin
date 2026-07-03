"""BaseModel shared by all entities — mirrors NodeAdmin's CreateDateColumn/UpdateDateColumn pattern."""
import uuid
from django.db import models


class BaseModel(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=lambda: str(uuid.uuid4()), editable=False)
    created_by = models.CharField(max_length=36, default='')
    updated_by = models.CharField(max_length=36, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
