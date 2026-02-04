from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.services.registration import register_user


User = get_user_model()


class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message=_("Пользователь с таким email уже существует"),
            )
        ],
    )

    full_name = serializers.CharField(
        required=True,
        max_length=255,
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        min_length=8,
    )

    password2 = serializers.CharField(
        write_only=True,
        required=True,
    )

    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": _("Пароли не совпадают")}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")

        result = register_user(
            email=validated_data["email"],
            full_name=validated_data["full_name"],
            password=validated_data["password"],
        )

        # сохраняем результат сервиса
        self._tokens = {
            "access": result["access"],
            "refresh": result["refresh"],
        }

        return result["user"]

    def to_representation(self, instance):
        data = {
            "email": instance.email,
            "full_name": instance.full_name,
            **self._tokens,
        }
        return data
