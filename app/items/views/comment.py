from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404, render

from ..forms import CommentForm
from ..models import Item, ItemComment

__all__ = (
    'comment_create',
    'comment_delete',
)


@login_required
def comment_create(request, item_pk):
    if not request.user.is_authenticated:
        return redirect('members:login')

    item = get_object_or_404(Item, pk=item_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.item = item
            comment.save()

            next_url = request.GET.get('next_url', '').strip()
            if next_url:
                return redirect(next_url)

            return redirect('items:public-item-detail', item_pk=item_pk)


@login_required
def comment_delete(request, comment_pk):
    next_url = request.GET.get('next_url', '').strip()

    if request.method == 'POST':
        comment = get_object_or_404(ItemComment, pk=comment_pk)
        if comment.user == request.user:
            comment.delete()
            if next_url:
                return redirect(next_url)
            return redirect('items:public-item-detail', item_pk=comment.item.pk)
        else:
            raise PermissionDenied('권한이 없습니다')
