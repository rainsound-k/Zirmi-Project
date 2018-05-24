from django.contrib.auth import get_user_model
from django.db import models

from core.models import TimeStampedModel
from . import Item

User = get_user_model()

__all__ = (
    'ItemComment',
)


class ItemComment(TimeStampedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    item = models.ForeignKey(
        Item,
        related_name='comments',
        on_delete=models.CASCADE,
    )
    content = models.TextField('')

    class Meta:
        ordering = ['created_time']
