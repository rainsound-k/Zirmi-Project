from django.db.models import Q
from django.shortcuts import render

from reviews.models import Review


def search_review(request):
    search_text = request.GET.get('search-text')
    search_type = request.GET.get('search-type')
    context = {}

    if search_text:
        if search_type == 'title':
            reviews = Review.objects.filter(title__contains=search_text)
        elif search_type == 'content':
            reviews = Review.objects.filter(content__contains=search_text)
        elif search_type == 'item':
            reviews = Review.objects.filter(item__name__contains=search_text)
        else:
            reviews = Review.objects.filter(
                Q(title__contains=search_text) | Q(content__contains=search_text) | Q(item__name__contains=search_text)
            )
    else:
        reviews = Review.objects.all()

    context = {
        'reviews': reviews,
        'search_text': search_text,
    }

    return render(request, 'reviews/review_list.html', context)
