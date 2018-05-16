from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

__all__ = (
    'login_view',
)


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            print(request.user.is_authenticated)
            if not request.user.is_authenticated:
                print('인증실패' + user.email)
            else:
                print('인증성공')
            return redirect('index')
    return render(request, 'members/login.html')
