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
        url = request.POST['purchase_url']
        Item.objects.add_from_search(request, url)
        return redirect('items:my-item-list')
