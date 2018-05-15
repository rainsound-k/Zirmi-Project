from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.views import login
from django.shortcuts import redirect, render

from ..forms import SignUpForm

User = get_user_model()

__all__ = (
    'signup_view',
)


def signup_view(request):
    context = {
        'errors': [],
    }

    signup_form = SignUpForm()
    context['signup_form'] = signup_form

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.email = form.cleaned_data['email']
            user.generation = form.cleaned_data['generation']
            user.gender = form.cleaned_data['gender']
            user.save()
            user.username = form.cleaned_data['username']
            user.password = form.cleaned_data['password1']

            user = authenticate(username=user.username, password=user.password)
            login(request, user)

            return redirect('index')
    else:
        form = SignUpForm()
    context = {
        'signup_form': form,
    }
    return render(request, 'members/signup.html', context)
