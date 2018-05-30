from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from ..forms import ItemForm
from ..models import Item

__all__ = (
    'item_add',
)


@login_required
def item_add(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            url = request.POST['purchase_url']
            Item.objects.add_from_search(request, url)
            return redirect('items:my-item-list')
    else:
        form = ItemForm()

    context = {
        'form': form,
    }

    return render(request, 'items/my_item/item_search.html', context)
