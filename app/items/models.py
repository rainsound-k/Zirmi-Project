from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class ItemManager(models.Manager):
    def add_from_public(self, item_pk, request):
        public_item = Item.objects.get(pk=item_pk)
        item, item_created = self.get_or_create(
            pk=item_pk,
            # user=request.user,
            defaults={
                'user': request.user,
                'name': public_item.name,
                'purchase_url': public_item.purchase_url,
                'price': public_item.price,
                'category': public_item.category,
                'img': public_item.img,
                # 'public_visibility': False,
            }

        )
        return item, item_created


class Item(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    name = models.CharField('상품명', max_length=50)
    purchase_url = models.URLField('상품 URL', max_length=200, blank=True)
    price = models.IntegerField('상품 가격')
    category = models.CharField('상품 카테고리', max_length=100, blank=True)
    img = models.ImageField('상품 이미지', upload_to='items', blank=True)
    public_visibility = models.BooleanField('공개 여부', default=True)
    created_date = models.DateTimeField(auto_now_add=True)
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
