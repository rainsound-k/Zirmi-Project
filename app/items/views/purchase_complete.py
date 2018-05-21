from django.shortcuts import redirect

from ..models import Item

__all__ = (
    'purchase_complete',
)


def purchase_complete(request, item_pk):
    if request.method == 'POST':
        Item.objects.purchase_complete(item_pk)
        return redirect('items:my-item-list')
