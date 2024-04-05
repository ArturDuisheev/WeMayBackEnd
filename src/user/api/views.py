from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from rest_framework.views import APIView

from core.settings.base import CLIENT_ID, CLIENT_SECRET

from django.db import transaction
from drf_social_oauth2.views import TokenView, RevokeTokenView, ConvertTokenView

from rest_framework.response import Response
from rest_framework import status, generics, permissions

from core.settings.local import BASE_URL
from user.api.serializers import AuthUserSerializer, CustomUserSerializer
from user import models as us_mod
from user.models import MyUser
from user.services import UserService


class RegisterAPIView(TokenView):
    queryset = us_mod.MyUser.objects.all()
    serializer_class = AuthUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            try:
                serializer.save()
            except Exception:
                transaction.set_rollback(True)
                return Response({
                    "message": "Произошла ошибка при регистрации пользователя"}
                    , status=status.HTTP_400_BAD_REQUEST
                )

            request.data['username'] = request.data.pop('email')
            request.data['client_id'] = CLIENT_ID
            request.data['client_secret'] = CLIENT_SECRET
            request.data['grant_type'] = 'password'
            print(request.data['grant_type'])
            tokens = super().post(request, *args, **kwargs)

            if tokens.status_code != status.HTTP_200_OK:
                transaction.set_rollback(True)
                return Response({
                    "message": "Произошла ошибка при регистрации пользователя"}
                    , status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "message": "Вы успешно зарегистрировались!",
             **tokens.data},
            status=status.HTTP_201_CREATED
        )


class LoginAPIView(TokenView):
    queryset = us_mod.MyUser.objects.all()

    def post(self, request, *args, **kwargs):
        request.data['username'] = request.data.pop('email')
        request.data['client_id'] = CLIENT_ID
        request.data['client_secret'] = CLIENT_SECRET
        request.data['grant_type'] = 'password'
        tokens = super().post(request, *args, **kwargs)

        if tokens.status_code != 200:
            return Response(
                tokens.data,
                status.HTTP_400_BAD_REQUEST
            )

        return Response({
            "message": "Вы успешно вошли в систему!",
             **tokens.data},
            status=status.HTTP_201_CREATED
        )


class LogoutAPIView(RevokeTokenView):
    queryset = us_mod.MyUser.objects.all()

    def post(self, request, *args, **kwargs):
        request.data['client_id'] = CLIENT_ID
        request.data['client_secret'] = CLIENT_SECRET
        request.data['grant_type'] = 'password'
        super().post(request, *args, **kwargs)

        return Response({
            "message": "Вы успешно вышли из системы!"},
            status=status.HTTP_201_CREATED
        )


class FacebookOAuthAPIView(APIView):
    def get(self, request):
        code = request.query_params.get('code')

        if not code:
            return Response(
                data={"message": "Authorization code is missing"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token_response = UserService.exchange_code_for_tokens_facebook(authorization_code=code).json()

        if 'error' in token_response:
            return Response(
                data={"message": token_response.get("error_description")},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        access_token = token_response.get('access_token')
        user_info = UserService.get_user_info_from_facebook(access_token=access_token)

        if 'error' in user_info:
            return Response(
                data={"message": user_info.get("error_description")},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user, created = MyUser.objects.get_or_create(
            email=user_info["email"],
            defaults={
                'email': user_info["email"],
                'password': make_password(MyUser.objects.make_random_password()),
                'username': user_info.get("name"),
                'fullname': user_info.get("name"),
                'is_active': True
            }
        )

        redirect_url = f'{BASE_URL}'  # TODO: сменить урл
        return HttpResponseRedirect(redirect_url)


class GoogleOAuthAPIView(APIView):
    def get(self, request):
        code = request.query_params.get('code')

        if not code:
            return Response(
                data={"message": "Authorization code is missing"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token_response = UserService.exchange_code_for_tokens(authorization_code=code).json()

        if 'error' in token_response:
            return Response(
                data={"message": token_response.get("error_description")},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        access_token = token_response.get('access_token')
        user_info = UserService.get_user_info_from_google(access_token=access_token)

        if 'error' in user_info:
            return Response(
                data={"message": user_info.get("error_description")},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user, created = MyUser.objects.get_or_create(
            email=user_info["email"],
            defaults={
                'email': user_info["email"],
                'password': make_password(MyUser.objects.make_random_password()),
                'username': user_info.get("name"),
                'fullname': user_info.get("name"),
                'is_active': True
            }
        )

        redirect_url = f'{BASE_URL}'  # TODO: сменить урл
        return HttpResponseRedirect(redirect_url)


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
