from django.contrib.auth import authenticate, logout, login

from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db import utils as django_utils
from user.api.serializers import RegisterSerializer, LogInSerializer


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        try:
            if not serializer.is_valid():
                return Response({'message': 'Неверный формат электронной почты'})
            serializer.save()
            return Response({"message": "Вы успешно зарегистрировались!"}, status=status.HTTP_201_CREATED)
        except django_utils.IntegrityError:
            return Response({'error': 'Неверный email'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'message': 'Ошибка при регистрации'})


class LogInView(APIView):
    def post(self, request):
        serializer = LogInSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'message': 'Неверный формат электронной почты'})

        user = authenticate(**serializer.validated_data)

        if not user:
            return Response({'detail': 'Неверные данные, попробуйте ещё раз!'}, status=status.HTTP_400_BAD_REQUEST)

        login(request, user)

        return Response(data={'message': 'Вход в систему выполнен успешно'})


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Perform logout
        logout(request)

        return Response({'message': 'Выход из системы выполнен успешно.'}, status=status.HTTP_200_OK)
