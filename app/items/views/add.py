from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from ..models import Item

__all__ = (
    'item_add',
)


@login_required
def item_add(request):
    if not request.user.is_authenticated:
        return redirect('members:login')

    if request.method == 'POST':
        Item.objects.add_from_search(request)
        return redirect('items:my-item-list')
