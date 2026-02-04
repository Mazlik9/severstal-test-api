from rest_framework import serializers
from users.models import User


class UserAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("avatar",)

    def validate_avatar(self, value):
        max_size = 5 * 1024 * 1024  # 5 MB

        if value.size > max_size:
            raise serializers.ValidationError("Размер изображения не должен превышать 5MB")

        if value.content_type not in ("image/jpeg", "image/png", "image/webp"):
            raise serializers.ValidationError("Допустимые форматы: jpeg, png, webp")

        return value
