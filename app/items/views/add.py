from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from ..forms import ItemForm

__all__ = (
    'item_add',
)


@login_required
def item_add(request):
    if not request.user.is_authenticated:
        return redirect('members:login')

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            return redirect('items:my-item-list')
    else:
        form = ItemForm()
    context = {
        'form': form,
    }
    return render(request, 'items/my_item/item_add.html', context)
