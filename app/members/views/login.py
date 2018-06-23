from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import redirect, render, render_to_response

User = get_user_model()

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
        if not user:
            if User.objects.filter(email=email):
                context = {
                    'error': '비밀번호가 틀렸습니다',
                }
            else:
                context = {
                    'error': '없는 이메일입니다. 회원가입 해주세요',
                }
            return render(request, 'members/login.html', context)
        else:
            login(request, user)
            # next url 있을 경우 next url로 redirect 설정
            if next_url:
                return redirect(next_url)
            return redirect('index')
    return render(request, 'members/login.html')
