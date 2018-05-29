from django.core.paginator import Paginator
from django.shortcuts import render

from ..models import Review

__all__ = (
    'review_list',
)


def review_list(request):
    reviews_list = Review.objects.all()
    paginator = Paginator(reviews_list, 30)
    paginator_num = range(1, paginator.num_pages + 1)
    page = request.GET.get('page')
    reviews = paginator.get_page(page)

    context = {
        'reviews': reviews,
        'paginator_num': paginator_num,
    }
    return render(request, 'reviews/review_list.html', context)
