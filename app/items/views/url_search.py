from django.shortcuts import render

from utils.check_url_from_url_parser import CheckURL
from ..forms import ItemForm
from ..models.item import Item

__all__ = (
    'search_url',
)


def search_url(request):
    url = request.GET.get('url')
    context = {}

    if url:
        search_result = CheckURL(url)
        search_result.check_url_from_parser()

        item_img = search_result.item_data.item_img
        item_price = search_result.item_data.item_price
        item_name = search_result.item_data.item_name
        url = search_result.item_data.url
        form = ItemForm()

        context = {
            'form': form,
            'category_choices': Item.CHOICES_CATEGORY,
            'item_img': item_img,
            'item_price': item_price,
            'item_name': item_name,
            'url': url,
        }
    return render(request, 'items/my_item/item_search.html', context)
