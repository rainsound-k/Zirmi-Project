from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import ReviewForm
from ..models import Review


@login_required
def review_edit(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user != review.user:
        raise PermissionDenied('권한이 없습니다')

    if request.method == 'POST':
        form = ReviewForm(request, request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            return redirect('reviews:review-list')
    else:
        form = ReviewForm(request, instance=review)
    context = {
        'form': form,
    }
    return render(request, 'reviews/review_edit.html', context)
