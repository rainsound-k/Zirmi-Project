from django.shortcuts import render

from ..models import Review

__all__ = (
    'review_list',
)


def review_list(request):
    reviews = Review.objects.all()
    context = {
        'reviews': reviews,
    }
    return render(request, 'reviews/review_list.html', context)
