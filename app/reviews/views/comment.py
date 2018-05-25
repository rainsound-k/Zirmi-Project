from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404

from ..forms import ReviewCommentForm
from ..models import ReviewComment, Review

__all__ = (
    'comment_create',
    'comment_delete',
)


@login_required
def comment_create(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'POST':
        form = ReviewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.review = review
            comment.save()

            next_url = request.GET.get('next_url', '').strip()
            if next_url:
                return redirect(next_url)

            return redirect('reviews:review-detail', review_pk=review_pk)


@login_required
def comment_delete(request, comment_pk):
    next_url = request.GET.get('next_url', '').strip()

    if request.method == 'POST':
        comment = get_object_or_404(ReviewComment, pk=comment_pk)
        if comment.user == request.user:
            comment.delete()
            if next_url:
                return redirect(next_url)
            return redirect('reviews:review-detail', review_pk=comment.review.pk)
        else:
            raise PermissionDenied('권한이 없습니다')
