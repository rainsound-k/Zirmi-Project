from datetime import datetime
from urllib.parse import urlparse

from django.core.files import File
from django.db import models

from utils.check_url_from_url_parser import CheckURL
from utils.file import download, get_buffer_ext

__all__ = (
    'ItemManager',
)


class ItemManager(models.Manager):
    def add_from_public(self, item_pk, request):
        from .item import Item
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

    def add_from_search(self, request, url):
        search_result = CheckURL(url)
        search_result.check_url_from_parser()

        item_category = request.POST['category']
        item_img = request.FILES.get('img', '')
        item_public_visibility = request.POST['public_visibility']
        item_price = request.POST['price'].replace(',', '')
        item_name = request.POST['name']
        if item_public_visibility == 'on' or item_public_visibility:
            item_public_visibility = True
        else:
            item_public_visibility = False

        item = self.create(
            user=request.user,
            name=item_name,
            purchase_url=search_result.item_data.url,
            price=item_price,
            category=item_category,
            img=item_img,
            public_visibility=item_public_visibility,
        )

        if not item.img and search_result.item_data.item_img:
            item_img_url = search_result.item_data.item_img
            temp_file = download(item_img_url)
            file_name = '{urlparse}.{ext}'.format(
                urlparse=urlparse(item_img_url).path.split('/')[-1].split('.')[0],
                ext=get_buffer_ext(temp_file)
            )
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
