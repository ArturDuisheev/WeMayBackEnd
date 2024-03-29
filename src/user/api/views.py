from core.settings.base import CLIENT_ID, CLIENT_SECRET

from django.db import transaction
from drf_social_oauth2.views import TokenView, RevokeTokenView, ConvertTokenView

from rest_framework.response import Response
from rest_framework import status, generics, permissions

from user.api.serializers import AuthUserSerializer, CustomUserSerializer
from user import models as us_mod


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


class FacebookOAuthAPIView(ConvertTokenView):
    queryset = us_mod.MyUser.objects.all()

    def post(self, request, *args, **kwargs):
        request.data['client_id'] = CLIENT_ID
        request.data['client_secret'] = CLIENT_SECRET
        request.data['grant_type'] = 'convert_token'
        request.data['backend'] = 'facebook'
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
    
from social_core.backends.google import GoogleOAuth2
from social_core.exceptions import AuthFailed
from social_django.utils import load_backend, load_strategy

class GoogleOAuthAPIView(ConvertTokenView):

    def post(self, request, *args, **kwargs):
        access_token = request.data.get('access_token')

        if not access_token:
            return Response({"error": "Access token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            backend = load_backend(load_strategy(request), GoogleOAuth2.name, None)
            user = backend.do_auth(access_token)
        except AuthFailed as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Failed to authenticate"}, status=status.HTTP_400_BAD_REQUEST)


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
