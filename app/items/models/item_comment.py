from django.contrib.auth import get_user_model
from django.db import models

from . import Item

User = get_user_model()

__all__ = (
    'ItemComment',
)


class ItemComment(models.Model):
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
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_date']
