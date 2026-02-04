import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:

    def test_create_user(self):
        user = User.objects.create_user(
            email="user@example.com",
            full_name="Test User",
            password="strong-password-123"
        )

        assert user.email == "user@example.com"
        assert user.full_name == "Test User"
        assert user.check_password("strong-password-123")

    def test_slug_is_generated(self):
        user = User.objects.create_user(
            email="slug@example.com",
            full_name="Slug User",
            password="password"
        )

        assert user.slug is not None
        assert len(user.slug) > 0

    def test_str_representation(self):
        user = User.objects.create_user(
            email="string@example.com",
            full_name="String User",
            password="password"
        )

        assert str(user) == "string@example.com"

    def test_default_fields(self):
        user = User.objects.create_user(
            email="defaults@example.com",
            full_name="Defaults User",
            password="password"
        )

        assert user.gender == User.Gender.OTHER
        assert user.is_active is True
        assert user.is_staff is False

    def test_get_full_name(self):
        user = User.objects.create_user(
            email="fullname@example.com",
            full_name="Full Name User",
            password="password"
        )

        assert user.get_full_name() == "Full Name User"

    def test_get_short_name(self):
        user = User.objects.create_user(
            email="shortname@example.com",
            full_name="Short Name User",
            password="password"
        )

        assert user.get_short_name() == "Short Name User"

    def test_email_is_unique(self):
        User.objects.create_user(
            email="unique@example.com",
            full_name="User One",
            password="password"
        )

        with pytest.raises(IntegrityError):
            User.objects.create_user(
                email="unique@example.com",
                full_name="User Two",
                password="password"
            )

