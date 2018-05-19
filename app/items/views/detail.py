from django.shortcuts import get_object_or_404, render

from ..forms import CommentForm
from ..models import Item

__all__ = (
    'item_detail',
    'public_item_detail',
)


def item_detail(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)
    comment_form = CommentForm()
    context = {
        'item': item,
        'comment_form': comment_form,
    }
    return render(request, 'items/item_detail.html', context)


def public_item_detail(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)
    comment_form = CommentForm()
    context = {
        'item': item,
        'comment_form': comment_form,
    }
    return render(request, 'items/public_item_detail.html', context)
