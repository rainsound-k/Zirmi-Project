import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_POST

from ..models import Item

__all__ = (
    'add_from_public',
)


@login_required(login_url='/login/')
@require_POST
def add_from_public(request):
    item_pk = request.POST.get('pk', None)
    Item.objects.add_from_public(item_pk, request)
    message = '내 아이템에 추가되었습니다'
    context = {
        'message': message,
    }
    return HttpResponse(json.dumps(context), content_type='application/json')
