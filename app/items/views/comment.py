import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.views.decorators.http import require_POST

from ..forms import CommentForm
from ..models import Item, ItemComment

__all__ = (
    'comment_create',
    'comment_delete',
)


@login_required
@require_POST
def comment_create(request):
    item_pk = request.POST.get('pk', None)
    next_path = request.POST.get('next_path', None)
    item = get_object_or_404(Item, pk=item_pk)
    comment_count = item.comments.count()
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.item = item
        comment.save()
        context = {
            'comment': comment,
            'comment_count': comment_count,
        }
        return render(request, 'items/new_comment.html', context)
    return redirect(next_path)


@login_required
@require_POST
def comment_delete(request):
    comment_pk = request.POST.get('comment_pk', None)
    comment = get_object_or_404(ItemComment, pk=comment_pk)
    item_pk = request.POST.get('item_pk', None)
    item = get_object_or_404(Item, pk=item_pk)
    # comment를 delete 하기 때문에 1을 빼줌
    comment_count = item.comments.count() - 1

    if comment.user == request.user:
        comment.delete()
        status = 1
        message = '삭제완료'
    else:
        status = 0
        message = '잘못된 접근입니다'

    context = {
        'status': status,
        'message': message,
        'comment_count': comment_count,
    }

    return HttpResponse(json.dumps(context), content_type='application/json')
