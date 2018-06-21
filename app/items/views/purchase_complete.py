import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_POST

from ..models import Item

__all__ = (
    'purchase_complete',
)


@login_required(login_url='/login/')
@require_POST
def purchase_complete(request):
    item_pk = request.POST.get('pk', None)
    Item.objects.purchase_complete(item_pk)
    message = '지르시느라 고생 많으셨습니다'
    context = {
        'message': message,
    }
    return HttpResponse(json.dumps(context), content_type='application/json')
