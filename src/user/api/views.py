from django.db import transaction
from drf_social_oauth2.views import TokenView

from rest_framework.response import Response
from rest_framework import status

from user.api.serializers import RegisterSerializer
from user import models as us_mod


class RegisterAPIView(TokenView):
    queryset = us_mod.MyUser.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
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
