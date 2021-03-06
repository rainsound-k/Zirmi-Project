from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

User = get_user_model()

__all__ = (
    'SignUpForm',
)


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.pop('autofocus', None)

    class Meta:
        model = User
        fields = (
            'email',
            'password1',
            'password2',
            'generation',
            'gender',
            'username',
        )

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise ValidationError('이미 사용중인 이메일입니다')
        return data

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise ValidationError('비밀번호와 비밀번호 확인란이 같지 않습니다')
        return password2

    def signup(self, request, user):
        user.gender = self.cleaned_data['gender']
        user.generation = self.cleaned_data['generation']
        user.save()
