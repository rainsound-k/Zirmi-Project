from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import ItemForm
from ..models import Item


@login_required(login_url='/login/')
def item_edit(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)
    if request.user != item.user:
        raise PermissionDenied('권한이 없습니다')

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
    return render(request, 'items/my_item/item_edit.html', context)
