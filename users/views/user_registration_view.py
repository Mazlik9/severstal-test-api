from rest_framework.generics import CreateAPIView
from drf_spectacular.utils import extend_schema
from users.serializers import UserRegistrationSerializer


@extend_schema(
    tags=['user'],
    summary='Регистрация пользователя',
    description='Регистрация пользователя и получение JWT токенов'
)
class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
