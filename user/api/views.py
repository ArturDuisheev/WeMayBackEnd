from django.contrib.auth import authenticate, logout, login
from drf_social_oauth2.views import TokenView

from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db.utils import IntegrityError
from user.api.serializers import RegisterSerializer, LoginSerializer
from user.models import MyUser


class RegisterAPIView(TokenView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        queryset = MyUser.objects.all()
        try:
            if queryset.filter(email=request.data['email']).exists():
                return Response({'message': 'Пользователь с таким email уже существует'})
            if not serializer.is_valid():
                return Response({'message': 'Неверный формат электронной почты'})
            serializer.save()

            # Prepare the data for getting tokens
            request.data['username'] = request.data.pop('email')
            request.data['grant_type'] = 'password'
            tokens = super().post(request, args, kwargs)

            return Response({"message": "Вы успешно зарегистрировались!", **tokens.data}, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'message': 'Ошибка при регистрации'})


# Deprecated
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'message': 'Неверный формат электронной почты'})

        user = authenticate(**serializer.validated_data)

        if not user:
            return Response({'detail': 'Неверные данные, попробуйте ещё раз!'}, status=status.HTTP_400_BAD_REQUEST)

        login(request, user)

        return Response(data={'message': 'Вход в систему выполнен успешно'})


# Deprecated
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Perform logout
        logout(request)

        return Response({'message': 'Выход из системы выполнен успешно.'}, status=status.HTTP_200_OK)
