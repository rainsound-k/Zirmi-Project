from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST

from ..models import Item

__all__ = (
    'item_delete',
)


@require_POST
def item_delete(request, item_pk):
    if not request.user.is_authenticated:
        return redirect('members:login')

    if request.method == 'POST':
        item = get_object_or_404(Item, pk=item_pk)
        if item.user == request.user:
            item.delete()
            return redirect('items:my-item-list')
        else:
            raise PermissionDenied('권한이 없습니다')
