import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from ..models import Review

__all__ = (
    'review_delete',
)


@login_required
@require_POST
def review_delete(request):
    review_pk = request.POST.get('pk', None)
    review = get_object_or_404(Review, pk=review_pk)
    if review.user == request.user:
        review.delete()
        message = '리뷰가 삭제되었습니다'
        context = {
            'message': message,
        }
        return HttpResponse(json.dumps(context), content_type='application/json')
