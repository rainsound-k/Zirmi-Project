from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

__all__ = (
    'login_view',
)


def login_view(request):
    # next url 가져옴
    next_url = request.GET.get('next')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            # next url 있을 경우 next url로 redirect 설정
            if next_url:
                return redirect(next_url)
            return redirect('index')
    return render(request, 'members/login.html')
