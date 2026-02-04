import uuid
from django.core.files.storage import default_storage
from rest_framework import serializers
from users.models import User


class UserAvatarSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(
        required=True,
        allow_empty_file=False,
        max_length=255
    )

    class Meta:
        model = User
        fields = ['avatar']

    def update(self, instance, validated_data):
        avatar_file = validated_data.get('avatar')

        if avatar_file:
            # Удаляем старый аватар, если он есть и не является дефолтным
            if instance.avatar and instance.avatar.name and "default_avatar.jpg" not in instance.avatar.name:
                try:
                    default_storage.delete(instance.avatar.name)
                except Exception as e:
                    print(f"Ошибка при удалении старого аватара: {e}")

            ext = avatar_file.name.split('.')[-1].lower() if '.' in avatar_file.name else 'jpg'
            unique_filename = f"user_{instance.id}/{uuid.uuid4().hex}.{ext}"

            instance.avatar.save(unique_filename, avatar_file, save=False)
            instance.save()

        return instance

    def validate_avatar(self, value):
        max_size = 5 * 1024 * 1024  # 5 MB
        allowed_extensions = ['jpg', 'jpeg', 'png', 'webp']
        allowed_mime_types = ['image/jpeg', 'image/png', 'image/webp']

        if value.size > max_size:
            raise serializers.ValidationError("Размер изображения не должен превышать 5MB")

        file_name = value.name.lower()
        if not any(file_name.endswith(ext) for ext in allowed_extensions) or value.content_type not in allowed_mime_types:
            raise serializers.ValidationError("Допустимые форматы: jpeg, png, webp")

        return value
