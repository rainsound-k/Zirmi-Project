from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from ..models import Item

__all__ = (
    'add_from_public',
)


@login_required
def add_from_public(request, item_pk):
    if not request.user.is_authenticated:
        return redirect('members:login')

    if request.method == 'POST':
        Item.objects.add_from_public(item_pk, request)
        return redirect('index')
