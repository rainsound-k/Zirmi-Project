from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import render, redirect

from .models import Review
from .forms import AddReviewForm


@login_required
def add_review(request):
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
    return render(request, 'reviews/post_review.html', context)


def review_list(request):
    reviews = Review.objects.all()
    context = {
        'reviews': reviews,
    }
    return render(request, 'reviews/review_list.html', context)


def view_review(request, review_pk):
    # view 수 증가
    view = Review.objects.filter(pk=review_pk)
    view.update(view_count=F('view_count') + 1)

    review = Review.objects.get(pk=review_pk)
    context = {
        'review': review,
    }
    return render(request, 'reviews/view_review.html', context)
