from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from ..forms import AddReviewForm

__all__ = (
    'review_add',
)


@login_required
def review_add(request):
    if request.method == 'POST':
        form = AddReviewForm(request, request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('reviews:review-list')
    else:
        form = AddReviewForm(request)
    context = {
        'form': form,
    }
    return render(request, 'reviews/review_add.html', context)
