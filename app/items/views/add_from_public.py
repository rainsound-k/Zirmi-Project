from django.shortcuts import redirect

from ..models import Item

__all__ = (
    'add_from_public',
)


def add_from_public(request, item_pk):
    if request.method == 'POST':
        Item.objects.add_from_public(item_pk, request)
        return redirect('index')
