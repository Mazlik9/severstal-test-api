from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema, OpenApiResponse

from users.serializers.user_self import UserAvatarSerializer
from users.permissions import IsAuthenticatedUserSelf


class UserAvatarUpdateView(APIView):
    permission_classes = [IsAuthenticatedUserSelf]
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(
        tags=["user"],
        summary="Обновление аватара пользователя",
        description="Загружает новое изображение аватара. Файл сохраняется в S3.",
        request=UserAvatarSerializer,
        responses={
            200: UserAvatarSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            401: OpenApiResponse(description="Не авторизован"),
        },
    )
    def patch(self, request):
        user = request.user
        serializer = UserAvatarSerializer(
            instance=user,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
