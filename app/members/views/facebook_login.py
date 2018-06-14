from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

__all__ = (
    'facebook_login',
)


def facebook_login(request):
    code = request.GET.get('code')
    user = authenticate(request, code=code)
    login(request, user)
    return redirect('index')
