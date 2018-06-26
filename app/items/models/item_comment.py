from django.contrib.auth import get_user_model
from django.db import models

from core.models import TimeStampedModel
from . import Item

User = get_user_model()

__all__ = (
    'ItemComment',
)


class ItemCommentManager(models.Manager):
    def no_reply_all(self):
        queryset = self.filter(parent=None)
        return queryset


class ItemComment(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    item = models.ForeignKey(Item, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField('')
    parent = models.ForeignKey('self', blank=True, null=True, related_name='replies', on_delete=models.CASCADE)

    objects = ItemCommentManager()

    class Meta:
        ordering = ['created_time']

    def children(self):
        return ItemComment.objects.filter(parent=self)

    def __str__(self):
        return f'{self.pk}. {self.content} - {self.user}'
