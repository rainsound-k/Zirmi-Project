from django.contrib.auth import get_user_model
from django.db import models

from core.models import TimeStampedModel
from ..models.managers import ItemManager

User = get_user_model()

__all__ = (
    'Item',
)


class Item(TimeStampedModel):
    CATEGORY_A = 'a'
    CATEGORY_B = 'b'
    CATEGORY_C = 'c'
    CATEGORY_D = 'd'
    CATEGORY_E = 'e'
    CATEGORY_F = 'f'
    CATEGORY_G = 'g'
    CATEGORY_H = 'h'
    CATEGORY_I = 'i'
    CATEGORY_J = 'j'
    CATEGORY_K = 'k'
    CHOICES_CATEGORY = (
        (CATEGORY_A, '패션의류/잡화'),
        (CATEGORY_B, '유아용품'),
        (CATEGORY_C, '뷰티'),
        (CATEGORY_D, '주방/생활용품'),
        (CATEGORY_E, '디지털/가전제품'),
        (CATEGORY_F, '가구/인테리어'),
        (CATEGORY_G, '운동용품'),
        (CATEGORY_H, '여행'),
        (CATEGORY_I, '도서/음반/공연'),
        (CATEGORY_J, '자동차용품'),
        (CATEGORY_K, '기타'),
    )

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
    category = models.CharField('상품 카테고리', max_length=100, choices=CHOICES_CATEGORY, blank=False)
    img = models.ImageField('상품 이미지', upload_to='items', blank=True)
    public_visibility = models.BooleanField('공개 여부', default=True)
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
        ordering = ['-created_time']

    def __str__(self):
        return self.name
