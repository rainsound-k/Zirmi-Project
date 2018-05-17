from django.contrib.auth import authenticate, get_user_model, login
from django.shortcuts import redirect, render

from ..forms import SignUpForm

User = get_user_model()

__all__ = (
    'signup_view',
)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            login(request, new_user)
            return redirect('items:index')
    else:
        form = SignUpForm()
    context = {
        'signup_form': form,
    }
    return render(request, 'members/signup.html', context)
