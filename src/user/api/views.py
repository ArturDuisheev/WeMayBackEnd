from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from drf_yasg.utils import swagger_auto_schema

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from rest_framework.response import Response
from rest_framework import status, generics, permissions

from core.settings.local import BASE_URL
from user.api.serializers import AuthUserSerializer, CustomUserSerializer
from user.models import MyUser
from user.services import UserService


class RegisterAPIView(APIView):
    serializer_class = AuthUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data
            email = user_data.get('email')
            password = user_data.get('password')
            username = user_data.get('username') if None else user_data.get('email')

            hashed_password = make_password(password)

            user, created = MyUser.objects.get_or_create(
                email=email,
                defaults={'username': username, 'password': hashed_password}
            )

            if created:
                tokens = UserService.generate_jwt_token(user)
                return Response({
                    "message": "You have been successfully registered!",
                    "tokens": tokens,
                    "uuid": user.id,
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "message": "User with this email already exists."
                }, status=status.HTTP_409_CONFLICT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        serializer = AuthUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(request, **serializer.validated_data)

        if user:
            login(request, user)
            access_token = AccessToken.for_user(user)
            refresh_token = RefreshToken.for_user(user)
            return Response(data={
                "message": "Вход в систему выполнен успешно",
                "tokens": {
                    "access": str(access_token),
                    "refresh": str(refresh_token)
                },
                "uuid": str(user.id)
            }, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Неверные данные, попробуйте ещё раз!'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logout Successful"}, status=status.HTTP_200_OK)


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
        print("code:", code)

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
        tokens = UserService.generate_jwt_token(user)

        redirect_url = f'{BASE_URL}'  # TODO: сменить урл
        return HttpResponseRedirect(redirect_url, headers={'Authorization': f'Bearer {tokens["access"]}'})


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def get_object(self):
    #     return self.request.user

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)

    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)
