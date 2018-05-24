from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import PostForm


@login_required
def new_post(request):
    form = PostForm(user=request.user)
    return render(request, 'reviews/post_review.html', {'form': form})


def review_list(request):
    context = {}
    return render(request, 'reviews/review_list.html', context)
