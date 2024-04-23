import requests
from .models import MyUser
from rest_framework.exceptions import NotFound
from django.db.models import Model
from decouple import config as env
from rest_framework_simplejwt.tokens import RefreshToken


class BaseService:
    model: Model

    @classmethod
    def fetch_one(cls, pk):
        try:
            return cls.model.objects.get(pk=pk)
        except cls.model.DoesNotExist:
            raise NotFound


class UserService(BaseService):
    model = MyUser

    @classmethod
    def generate_jwt_token(cls, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    @classmethod
    def get_user_info_from_google(cls, access_token):
        user_info_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
        headers = {'Authorization': f'Bearer {access_token}'}
        user_info_response = requests.get(user_info_url, headers=headers)
        return user_info_response.json()

    @classmethod
    def exchange_code_for_tokens(cls, authorization_code):
        token_url = 'https://oauth2.googleapis.com/token'
        token_data = {
            'code': authorization_code,
            'client_id': env('GOOGLE_CLIENT_ID'),
            'client_secret': env('GOOGLE_CLIENT_SECRET'),
            'redirect_uri': env('BASE_URL') + 'api/v1/users/oauth/google/',
            'grant_type': 'authorization_code'
        }

        response = requests.post(token_url, data=token_data)
        return response

    @classmethod
    def get_user_info_from_facebook(cls, access_token):
        user_info_url = 'https://graph.facebook.com/v12.0/me?fields=id,name,email'
        headers = {'Authorization': f'Bearer {access_token}'}
        user_info_response = requests.get(user_info_url, headers=headers)
        return user_info_response.json()

    @classmethod
    def exchange_code_for_tokens_facebook(cls, authorization_code):
        token_url = 'https://graph.facebook.com/v12.0/oauth/access_token'
        token_data = {
            'code': authorization_code,
            'client_id': env('FACEBOOK_APP_ID'),
            'client_secret': env('FACEBOOK_APP_SECRET'),
            'redirect_uri': env('BASE_URL') + 'api/v1/users/oauth/facebook/',
            'grant_type': 'authorization_code'
        }

        response = requests.post(token_url, data=token_data)
        return response
