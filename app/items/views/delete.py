import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from ..models import Item

__all__ = (
    'item_delete',
)


@login_required
@require_POST
def item_delete(request):
    item_pk = request.POST.get('pk', None)
    item = get_object_or_404(Item, pk=item_pk)
    if item.user == request.user:
        item.delete()
        message = '아이템이 삭제되었습니다'
        context = {
            'message': message,
        }
        return HttpResponse(json.dumps(context), content_type='application/json')
