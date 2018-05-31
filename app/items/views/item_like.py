import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from ..models import Item

__all__ = (
    'item_like_toggle',
)


@login_required
@require_POST
def item_like_toggle(request):
    item_pk = request.POST.get('pk', None)
    item = get_object_or_404(Item, pk=item_pk)
    item_like, item_like_created = item.like_user_info_list.get_or_create(user=request.user)

    if not item_like_created:
        item_like.delete()
        message = '좋아요 취소'
    else:
        message = '좋아요'

    like_count = item.like_users.count()
    if like_count > 1:
        like_count_text = f'{like_count} likes'
    else:
        like_count_text = f'{like_count} like'
    context = {
        'like_count_text': like_count_text,
        'message': message,
    }

    return HttpResponse(json.dumps(context), content_type='application/json')
