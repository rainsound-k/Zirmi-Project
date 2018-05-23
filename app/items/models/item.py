from django.contrib.auth import get_user_model
from django.db import models

from ..models.managers import ItemManager

User = get_user_model()

__all__ = (
    'Item',
)


class Item(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='user_items'
    )
    name = models.CharField('상품명', max_length=50)
    purchase_url = models.URLField('상품 URL', max_length=200, blank=True)
    price = models.IntegerField('상품 가격')
    category = models.CharField('상품 카테고리', max_length=100, blank=True)
    img = models.ImageField('상품 이미지', upload_to='items', blank=True)
    public_visibility = models.BooleanField('공개 여부', default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_purchase = models.BooleanField('구매 여부', default=False)
    purchase_date = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    like_users = models.ManyToManyField(
        User,
        through='ItemLike',
        related_name='like_items',
        blank=True
    )

    objects = ItemManager()

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.name

    def toggle_like_user(self, user):
        like, like_created = self.like_user_info_list.get_or_create(user=user)
        if not like_created:
            like.delete()
        return like_created
