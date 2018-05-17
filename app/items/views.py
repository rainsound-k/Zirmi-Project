from django.shortcuts import render

from .models import Item

__all__ = (
    'item_list',
    'my_item_list',
)


def item_list(request):
    items = Item.objects.all()
    context = {
        'items': items,
    }
    return render(request, 'index.html', context)


def my_item_list(request):
    my_items = Item.objects.filter(user=request.user)
    context = {
        'my_items': my_items,
    }
    return render(request, 'items/my_items_list.html', context)
