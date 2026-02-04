from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView,
)
from drf_spectacular.utils import extend_schema

@extend_schema(
    tags=['auth'],
    summary='Получение JWT токена',
    description='Получение access и refresh токенов по email и паролю'
)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema(
    tags=['auth'],
    summary='Обновление JWT токена',
    description='Получение нового access токена по refresh токену'
)
class CustomTokenRefreshView(TokenRefreshView):
    pass


@extend_schema(
    tags=['auth'],
    summary='Верификация JWT токена',
    description='Проверка валидности access токена'
)
class CustomTokenVerifyView(TokenVerifyView):
    pass


@extend_schema(
    tags=['auth'],
    summary='Черный список токенов',
    description='Добавление refresh токена в черный список (logout)'
)
class CustomTokenBlacklistView(TokenBlacklistView):
    pass