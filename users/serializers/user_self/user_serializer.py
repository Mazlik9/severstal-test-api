from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSelfSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'slug',
            'email',
            'phone',
            'full_name',
            'avatar',
            'gender',
            'birth_date',
            'is_active',
            'is_staff',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'slug',
            'is_active',
            'is_staff',
            'created_at',
            'updated_at',
        )

    def get_avatar(self, obj):
        if not obj.avatar:
            return None

        url = obj.avatar.url

        return str(url).replace("http://minio:9000", getattr(settings, "MINIO_PUBLIC_URL", "http://localhost:9000"))
