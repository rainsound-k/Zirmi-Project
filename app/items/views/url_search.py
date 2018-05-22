from django.shortcuts import render

from utils.url_parser import get_item_info_url

__all__ = (
    'search_url',
)


def search_url(request):
    url = request.GET.get('url')
    context = {}

    if url:
        # search_item = get_11st_item_info(url)
        search_item = get_item_info_url(url)
        item_img = search_item['item_img']
        item_price = search_item['item_price']
        item_name = search_item['item_name']
        url = url

        context = {
            'item_img': item_img,
            'item_price': item_price,
            'item_name': item_name,
            'url': url,
        }
    return render(request, 'items/my_item/item_search.html', context)
