from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from reviews.models import Review


def search_review(request):
    search_text = request.GET.get('search-text')
    search_type = request.GET.get('search-type')

    # search 후 다음 페이지 넘겨도 search 정보 유지
    get_copy = request.GET.copy()
    parameters = get_copy.pop('page', True) and get_copy.urlencode()

    if search_text:
        if search_type == 'title':
            reviews_list = Review.objects.filter(title__contains=search_text)
        elif search_type == 'content':
            reviews_list = Review.objects.filter(content__contains=search_text)
        elif search_type == 'item':
            reviews_list = Review.objects.filter(item__name__contains=search_text)
        else:
            reviews_list = Review.objects.filter(
                Q(title__contains=search_text) | Q(content__contains=search_text) | Q(item__name__contains=search_text)
            )
        paginator = Paginator(reviews_list, 30)
        paginator_num = range(1, paginator.num_pages + 1)
        page = request.GET.get('page')
        reviews = paginator.get_page(page)

    else:
        reviews_list = Review.objects.all()
        paginator = Paginator(reviews_list, 30)
        paginator_num = range(1, paginator.num_pages + 1)
        page = request.GET.get('page')
        reviews = paginator.get_page(page)

    today_date = datetime.now().strftime('%Y. %-m. %d')

    context = {
        'today_date': today_date,
        'reviews': reviews,
        'search_text': search_text,
        'paginator_num': paginator_num,
        'parameters': parameters,
    }

    return render(request, 'reviews/review_list.html', context)
