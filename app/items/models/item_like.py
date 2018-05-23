from django.contrib.auth import get_user_model
from django.db import models

from . import Item

User = get_user_model()

__all__ = (
    'ItemLike',
)


class ItemLike(models.Model):
    item = models.ForeignKey(
        Item,
        related_name='like_user_info_list',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        related_name='like_item_info_list',
        on_delete=models.CASCADE,
    )
    created_date = models.DateTimeField(auto_now_add=True)
