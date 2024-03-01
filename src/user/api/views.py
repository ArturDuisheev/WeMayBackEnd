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
        serializer.save()

        request.data['username'] = request.data.pop('email')
        tokens = super().post(request, *args, **kwargs)

        return Response({
            "message": "Вы успешно зарегистрировались!",
            **tokens.data},
            status=status.HTTP_201_CREATED
        )
