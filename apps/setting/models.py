import uuid
from django.db import models


def _uuid4_str():
    return str(uuid.uuid4())


class Setting(models.Model):
    class Meta:
        db_table = 'settings'

    id = models.CharField(max_length=36, primary_key=True, default=_uuid4_str, editable=False)
    initial = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    icon = models.CharField(max_length=255, null=True, blank=True)
    logo = models.CharField(max_length=255, null=True, blank=True)
    favicon = models.CharField(max_length=255, null=True, blank=True)
    login_image = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    copyright = models.CharField(max_length=255, null=True, blank=True)
    theme = models.CharField(max_length=20, default='Blue')
    fe_template = models.CharField(max_length=80, default='agency-consulting-002-creative-agency')
    created_by = models.CharField(max_length=36, default='')
    updated_by = models.CharField(max_length=36, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or 'Setting'
