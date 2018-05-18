from django.shortcuts import redirect

from ..models import Item

__all__ = (
    'item_like_toggle',
)


def item_like_toggle(request, item_pk):
    item = Item.objects.get(pk=item_pk)
    if request.method == 'POST':
        item.toggle_like_user(user=request.user)
        next_url = request.POST.get('next_url', 'index')
        return redirect(next_url)
