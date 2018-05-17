from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import ItemForm
from .models import Item

__all__ = (
    'item_list',
    'my_item_list',
    'item_add',
)


def item_list(request):
    items = Item.objects.filter(public_visibility=True)
    context = {
        'items': items,
    }
    return render(request, 'index.html', context)


@login_required
def my_item_list(request):
    if not request.user.is_authenticated:
        return redirect('members:login')

    my_items = Item.objects.filter(user=request.user)
    context = {
        'my_items': my_items,
    }
    return render(request, 'items/my_items_list.html', context)


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
    return render(request, 'items/item_add.html', context)
