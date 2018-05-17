from django.shortcuts import get_object_or_404, redirect, render

from ..forms import ItemForm
from ..models import Item


def item_edit(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('items:my-item-list')
    else:
        form = ItemForm(instance=item)
    context = {
        'form': form,
    }
    return render(request, 'items/item_edit.html', context)
