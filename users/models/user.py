import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models

from core.GUIDModel import GUIDModel
from users.utils import UserManager


class User(GUIDModel, AbstractBaseUser, PermissionsMixin):
    class Gender(models.TextChoices):
        MALE = "male", "Мужской"
        FEMALE = "female", "Женский"
        OTHER = "other", "Не указан"

    email = models.EmailField(unique=True, db_index=True)

    full_name = models.CharField(
        max_length=255,
        verbose_name="ФИО"
    )

    slug = models.SlugField(
        unique=True,
        editable=False,
        max_length=36,
        db_index=True,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\+?[1-9]\d{7,14}$',
                message='Номер телефона должен быть в формате +79991234567'
            )
        ],
        verbose_name='Телефон'
    )

    gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
        default=Gender.OTHER,
        verbose_name="Пол"
    )

    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата рождения"
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    avatar = models.ImageField(
        upload_to="users/avatars/",
        null=True,
        blank=True,
        default="users/avatars/default_avatar.jpg"
    )


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = uuid.uuid4().hex
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email


    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name
