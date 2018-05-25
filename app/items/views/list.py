from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ..forms import CommentForm
from ..models import Item

__all__ = (
    'item_list',
    'my_item_list',
    'my_complete_item_list',
)


def item_list(request):
    items = Item.objects.filter(public_visibility=True)
    comment_form = CommentForm()
    context = {
        'items': items,
        'comment_form': comment_form,
    }
    return render(request, 'index.html', context)


@login_required
def my_item_list(request):
    my_items = Item.objects.filter(user=request.user, is_purchase=False)
    total_cost = 0
    for my_item in my_items:
        total_cost += my_item.price

    context = {
        'my_items': my_items,
        'total_cost': total_cost,
    }
    return render(request, 'items/my_item/my_items_list.html', context)


@login_required
def my_complete_item_list(request):
    my_items = Item.objects.filter(user=request.user, is_purchase=True)
    total_cost = 0
    for my_item in my_items:
        total_cost += my_item.price

    context = {
        'my_items': my_items,
        'total_cost': total_cost,
    }
    return render(request, 'items/my_item/my_complete_items_list.html', context)
