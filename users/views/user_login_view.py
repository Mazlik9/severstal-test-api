from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

from users.serializers import UserLoginSerializer


@extend_schema(
    tags=["user"],
    summary="Авторизация пользователя",
    description=(
        "Авторизация пользователя по email или номеру телефона. "
        "В ответе возвращаются JWT access и refresh токены."
    ),
    request=UserLoginSerializer,
    responses={
        200: OpenApiResponse(
            description="Успешная авторизация",
            response={
                "type": "object",
                "properties": {
                    "email": {"type": "string", "example": "user@mail.com"},
                    "phone": {"type": "string", "example": "+79991234567"},
                    "full_name": {"type": "string", "example": "Иван Иванов"},
                    "access": {"type": "string", "example": "eyJ0eXAiOiJKV1Q..."},
                    "refresh": {"type": "string", "example": "eyJ0eXAiOiJKV1Q..."},
                },
            },
        ),
        400: OpenApiResponse(
            description="Неверный email/телефон или пароль",
        ),
        401: OpenApiResponse(
            description="Пользователь не авторизован",
        ),
    },
)
class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        return Response(
            {
                "email": user.email,
                "phone": user.phone,
                "full_name": user.full_name,
                "access": serializer.validated_data["access"],
                "refresh": serializer.validated_data["refresh"],
            },
            status=status.HTTP_200_OK,
        )
