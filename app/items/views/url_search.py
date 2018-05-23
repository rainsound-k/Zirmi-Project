from django.shortcuts import render

from utils.url_parser import ItemData

__all__ = (
    'search_url',
)


def search_url(request):
    url = request.GET.get('url')
    context = {}

    if url:
        item_data = ItemData(url)
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

        item_img = item_data.item_img
        item_price = item_data.item_price
        item_name = item_data.item_name
        url = item_data.url

        context = {
            'item_img': item_img,
            'item_price': item_price,
            'item_name': item_name,
            'url': url,
        }
    return render(request, 'items/my_item/item_search.html', context)
