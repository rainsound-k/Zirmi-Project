from django.db.models import F
from django.shortcuts import render

from ..forms import ReviewCommentForm
from ..models import Review

__all__ = (
    'review_detail',
)


def review_detail(request, review_pk):
    # view 수 증가
    view = Review.objects.filter(pk=review_pk)
    view.update(view_count=F('view_count') + 1)

    comment_form = ReviewCommentForm()
    review = Review.objects.get(pk=review_pk)
    context = {
        'review': review,
        'comment_form': comment_form,
    }
    return render(request, 'reviews/review_detail.html', context)
