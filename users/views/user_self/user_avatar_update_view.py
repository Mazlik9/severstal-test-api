from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from users.permissions import IsAuthenticatedUserSelf
from users.serializers.user_self import UserAvatarSerializer

@extend_schema(
    methods=['PATCH'],
    summary="Обновление аватара текущего пользователя.",
    description="Обновление аватара текущего пользователя. Максимальный размер файла 5MB.",
    request=UserAvatarSerializer,
    responses={
        200: UserAvatarSerializer,
        400: OpenApiResponse(description="Файл не найден или превышен размер"),
        401: OpenApiResponse(description="Требуется аутентификация"),
        500: OpenApiResponse(description="Ошибка при загрузке файла")
    },
    examples=[
        OpenApiExample(
            "Пример запроса",
            value={
                "avatar": "файл изображения"
            },
            request_only=True,
        ),
    ],
)
class UserAvatarUpdateView(generics.UpdateAPIView):
    """
    Обновление аватара текущего пользователя.
    Поддерживаются только файлы до 5 MB.
    """
    serializer_class = UserAvatarSerializer
    permission_classes = [IsAuthenticatedUserSelf]
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ['patch']

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        avatar_file = request.FILES.get('avatar')
        if not avatar_file:
            return Response(
                {"detail": "Файл аватара не найден. Используйте multipart/form-data."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if avatar_file.size > 5 * 1024 * 1024:  # 5 MB
            return Response(
                {"detail": "Размер файла превышает 5 MB"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().patch(request, *args, **kwargs)
