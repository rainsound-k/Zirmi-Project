from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import redirect, render

from ..forms import SignUpForm

User = get_user_model()

__all__ = (
    'facebook_signup',
)


def facebook_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            generation = form.cleaned_data['generation']
            gender = form.cleaned_data['gender']
            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                generation=generation,
                gender=gender,
            )
            new_user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            login(request, new_user)
            return redirect('index')
        else:
            form = SignUpForm()
        context = {
            'signup_form': form,
        }
        return render(request, 'members/facebook_signup.html', context)
