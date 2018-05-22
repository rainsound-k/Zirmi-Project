from datetime import datetime
from urllib.parse import urlparse

from django.contrib.auth import get_user_model
from django.core.files import File
from django.db import models

from utils.file import download
from utils.url_parser import get_item_info_url

User = get_user_model()


class ItemManager(models.Manager):
    def add_from_public(self, item_pk, request):
        public_item = Item.objects.get(pk=item_pk)
        if public_item.user == request.user:
            pass
        else:
            item = self.create(
                user=request.user,
                name=public_item.name,
                purchase_url=public_item.purchase_url,
                price=public_item.price,
                category=public_item.category,
                img=public_item.img,
                public_visibility=False,

            )
            return item

    @staticmethod
    def add_from_search(request):
        item_name = request.POST['name']
        item_purchase_url = request.POST['purchase_url']
        item_price = request.POST['price']
        item_category = request.POST['category']
        item_img = request.FILES.get('img', '')
        item_public_visibility = request.POST['public_visibility']
        if item_public_visibility == 'on':
            item_public_visibility = True
        else:
            item_public_visibility = False

        item = Item.objects.create(
            user=request.user,
            name=item_name,
            purchase_url=item_purchase_url,
            price=item_price,
            category=item_category,
            img=item_img,
            public_visibility=item_public_visibility,
        )

        if not item.img:
            search_item = get_item_info_url(item_purchase_url)
            item_img_url = search_item['item_img']
            temp_file = download(item_img_url)
            file_name = urlparse(item_img_url).path.split('/')[-1]
            item.img.save(file_name, File(temp_file))

        return item

    def purchase_complete(self, item_pk):
        item, created = self.update_or_create(
            pk=item_pk,
            defaults={
                'is_purchase': True,
                'purchase_date': datetime.now(),
            }
        )
        return item, created


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
