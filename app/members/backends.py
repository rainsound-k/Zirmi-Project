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
            facebook_id = response_dict['id']
            facebook_email = response_dict['email']
            facebook_age_range = response_dict['age_range']['min']
            if facebook_age_range:
                if facebook_age_range < 12:
                    facebook_age_range = 1
                elif facebook_age_range < 22:
                    facebook_age_range = 2
                elif facebook_age_range < 32:
                    facebook_age_range = 3
                elif facebook_age_range < 42:
                    facebook_age_range = 4
                else:
                    facebook_age_range = 5
            facebook_gender = response_dict['gender']
            if facebook_gender:
                if facebook_gender == 'male':
                    facebook_gender = 'm'
                elif facebook_gender == 'femal':
                    facebook_gender = 'f'
            user, _ = User.objects.get_or_create(
                username=facebook_id,
                email=facebook_email,
                gender=facebook_gender,
                generation=facebook_age_range
            )
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
