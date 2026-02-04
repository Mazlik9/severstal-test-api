from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.serializers.user_self import UserSelfSerializer
from users.permissions import IsAuthenticatedUserSelf


class UserSelfView(APIView):
    """
    Эндпоинт для работы с профилем текущего пользователя.
    GET    - получить свой профиль
    PATCH  - обновить редактируемые поля
    """
    permission_classes = [IsAuthenticatedUserSelf]

    @extend_schema(
        tags=['user-self'],
        summary='Получение профиля текущего пользователя',
        description='Возвращает данные текущего пользователя (slug, email, full_name, phone и т.д.)',
        responses=UserSelfSerializer
    )
    def get(self, request):
        serializer = UserSelfSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['user-self'],
        summary='Обновление профиля текущего пользователя',
        description='Позволяет изменить редактируемые поля профиля',
        request=UserSelfSerializer,
        responses=UserSelfSerializer
    )
    def patch(self, request):
        serializer = UserSelfSerializer(
            instance=request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
