from datetime import datetime
from urllib.parse import urlparse

from django.core.files import File
from django.db import models

from utils.file import download, get_buffer_ext
from utils.url_parser import ItemData

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
        item_data = ItemData(request, url)
        if '11st.co.kr' in url:
            item_data.get_info_from_11st()

        elif 'gmarket.co.kr' in url:
            item_data.get_info_from_gmarket()

        elif 'auction.co.kr' in url:
            item_data.get_info_from_auction()

        elif 'interpark.com' in url:
            item_data.get_info_from_interpark()

        elif 'smartstore.naver.com' in url:
            item_data.get_info_from_naver_store()

        elif 'naver.me' in url:
            item_data.get_info_from_naver_short_url()

        elif 'lotteimall.com' in url:
            item_data.get_info_from_lotte()

        elif 'hyundaihmall.com' in url:
            item_data.get_info_from_hyundai()

        item_category = request.POST['category']
        item_img = request.FILES.get('img', '')
        item_public_visibility = request.POST['public_visibility']
        if item_public_visibility == 'on' or item_public_visibility:
            item_public_visibility = True
        else:
            item_public_visibility = False

        item = self.create(
            user=request.user,
            name=item_data.item_name,
            purchase_url=item_data.url,
            price=item_data.item_price,
            category=item_category,
            img=item_img,
            public_visibility=item_public_visibility,
        )

        if not item.img and item_data.item_img:
            item_img_url = item_data.item_img
            temp_file = download(item_img_url)
            file_name = '{urlparse}.{ext}'.format(
                urlparse=urlparse(item_img_url).path.split('/')[-1],
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
