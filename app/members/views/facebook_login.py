import requests
from django.conf import settings
from django.contrib.auth import login, get_user_model
from django.shortcuts import redirect, render

from members.forms import SignUpForm

User = get_user_model()

__all__ = (
    'facebook_login',
)


def facebook_login(request):
    client_app_id = settings.FACEBOOK_APP_ID
    client_secret = settings.FACEBOOK_SECRET_CODE
    url_access_token = 'https://graph.facebook.com/v2.12/oauth/access_token'
    url_me = 'https://graph.facebook.com/v2.12/me'
    code = request.GET['code']

    redirect_uri = 'http://localhost:8000/facebook-login/'
    params_access_token = {
        'client_id': client_app_id,
        'redirect_uri': redirect_uri,
        'client_secret': client_secret,
        'code': code,
    }
    response = requests.get(url_access_token, params_access_token)
    response_dict = response.json()

    params = {
        'access_token': response_dict['access_token'],
        'fields': ','.join([
            'id',
            'name',
            'email',
            'age_range',
            'gender',
        ])
    }
    response = requests.get(url_me, params)
    response_dict = response.json()

    facebook_id = response_dict.get('id', None)
    facebook_email = response_dict.get('email', None)
    try:
        facebook_age_range = response_dict['age_range']['min']
    except KeyError:
        facebook_generation = ''
    else:
        if facebook_age_range < 12:
            facebook_generation = '1'
        elif facebook_age_range < 22:
            facebook_generation = '2'
        elif facebook_age_range < 32:
            facebook_generation = '3'
        elif facebook_age_range < 42:
            facebook_generation = '4'
        else:
            facebook_generation = '5'
    try:
        facebook_gender = response_dict['gender']
    except KeyError:
        facebook_gender = ''
    else:
        if facebook_gender == 'male':
            facebook_gender = 'm'
        elif facebook_gender == 'femal':
            facebook_gender = 'f'
    try:
        user = User.objects.get(username=facebook_id)
    except User.DoesNotExist:
        form = SignUpForm()
        context = {
            'signup_form': form,
            'facebook_id': facebook_id,
            'facebook_email': facebook_email,
            'facebook_generation': facebook_generation,
            'facebook_gender': facebook_gender,
        }
        return render(request, 'members/facebook_signup.html', context)
    else:
        login(request, user, backend='members.backends.FacebookBackend')
        return redirect('index')
