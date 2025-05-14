from django.contrib.auth.models import User
from django.db import models

from common.models import BasicModel


class Event(BasicModel):
    title = models.CharField(verbose_name="Title", max_length=256)
    description = models.TextField(verbose_name="Description")
    date = models.DateTimeField(verbose_name="Date")
    location = models.CharField(verbose_name="Location", max_length=1028)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    invited_users = models.ManyToManyField(User, related_name='invited_events', blank=True)
    registered_users = models.ManyToManyField(User, related_name='registered_events', blank=True)

    class Meta:
        db_table = 'event'
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return str(self.title) + " event"
