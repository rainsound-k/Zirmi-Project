import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


class APIFacebookBackend:
    CLIENT_APP_ID = settings.FACEBOOK_APP_ID
    CLIENT_SECRET_CODE = settings.FACEBOOK_SECRET_CODE

    def authenticate(self, request, access_token):
        params = {
            'access_token': access_token,
            'fields': ','.join([
                'id',
                'name',
                'email',
                'age_range',
                'gender',
            ])
        }
        response = requests.get('https://graph.facebook.com/v2.12/me', params)
        if response.status_code == status.HTTP_200_OK:
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
            if User.objects.filter(username=facebook_id):
                user = User.objects.get(username=facebook_id)
                return user
            else:
                user, _ = User.objects.get_or_create(
                    username=facebook_id,
                    email=facebook_email,
                    gender=facebook_gender,
                    generation=facebook_generation,
                )
                return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class FacebookBackend:
    CLIENT_ID = settings.FACEBOOK_APP_ID
    CLIENT_SECRET = settings.FACEBOOK_SECRET_CODE
    URL_ACCESS_TOKEN = 'https://graph.facebook.com/v2.12/oauth/access_token'
    URL_ME = 'https://graph.facebook.com/v2.12/me'

    def authenticate(self, request, code):
        def get_access_token(auth_code):
            redirect_uri = 'http://localhost:8000/facebook-login/'
            params_access_token = {
                'client_id': self.CLIENT_ID,
                'redirect_uri': redirect_uri,
                'client_secret': self.CLIENT_SECRET,
                'code': auth_code,
            }
            response = requests.get(self.URL_ACCESS_TOKEN, params_access_token)
            response_dict = response.json()
            return response_dict['access_token']

        def get_user_info(user_access_token):
            params = {
                'access_token': user_access_token,
                'fields': ','.join([
                    'id',
                    'name',
                    'email',
                ])
            }
            response = requests.get(self.URL_ME, params)
            response_dict = response.json()
            return response_dict

        access_token = get_access_token(code)
        user_info = get_user_info(access_token)

        facebook_id = user_info['id']

        try:
            user = User.objects.get(username=facebook_id)
        except User.DoesNotExist:
            return None
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
