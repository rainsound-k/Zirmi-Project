import json

from django.contrib.auth.decorators import login_required
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
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.item = item
        comment.save()
        context = {
            'comment': comment,
        }
        return render(request, 'items/new_comment.html', context)
    return redirect(next_path)


@login_required
@require_POST
def comment_delete(request):
    comment_pk = request.POST.get('pk', None)
    comment = get_object_or_404(ItemComment, pk=comment_pk)

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
    }

    return HttpResponse(json.dumps(context), content_type='application/json')
