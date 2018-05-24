from django.shortcuts import render

from .forms import PostForm


def new_post(request):
    form = PostForm(user=request.user)
    return render(request, 'reviews/post_review.html', {'form': form})
