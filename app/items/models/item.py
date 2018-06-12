from urllib.parse import urlparse

from django.contrib.auth import get_user_model
from django.core.files import File
from django.db import models

from core.models import TimeStampedModel
from utils.check_url_from_url_parser import CheckURL
from utils.file import download, get_buffer_ext
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
    purchase_url = models.URLField('상품 URL', max_length=400, blank=True)
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

    def save(self, *args, **kwargs):
        if Item.objects.filter(pk=self.pk):
            super().save()
        else:
            if self.purchase_url and not self.img:
                url = self.purchase_url
                search_result = CheckURL(url)
                search_result.check_url_from_parser()

                item_img_url = search_result.item_data.item_img
                if item_img_url:
                    temp_file = download(item_img_url)
                    file_name = '{urlparse}.{ext}'.format(
                        urlparse=urlparse(item_img_url).path.split('/')[-1].split('.')[0],
                        ext=get_buffer_ext(temp_file)
                    )
                    self.purchase_url = search_result.item_data.url
                    self.img.save(file_name, File(temp_file))
            super().save()

    def __str__(self):
        return f'{self.pk}. {self.name} - {self.user}'
