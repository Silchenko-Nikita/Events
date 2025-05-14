from django.db import models

from common.consts import OBJECT_STATUS_ACTIVE, OBJECT_STATUS_INACTIVE


class BasicModel(models.Model):
    STATUS_CHOICES = (
        (OBJECT_STATUS_ACTIVE, 'Active'),
        (OBJECT_STATUS_INACTIVE, 'Inactive'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=OBJECT_STATUS_ACTIVE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
