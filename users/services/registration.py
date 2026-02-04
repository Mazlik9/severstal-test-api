from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


@transaction.atomic
def register_user(*, email: str, full_name: str, password: str) -> dict:
    """
    Регистрирует пользователя и возвращает JWT-токены
    """

    user = User.objects.create_user(
        email=email,
        full_name=full_name,
        password=password,
    )

    refresh = RefreshToken.for_user(user)

    return {
        "user": user,
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }
