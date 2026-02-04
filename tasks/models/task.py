import uuid
from django.db import models
from django.utils.text import slugify
from django.conf import settings


class Task(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Активна"
        DONE = "done", "Завершена"

    slug = models.SlugField(
        max_length=36,
        unique=True,
        editable=False,
        db_index=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Генерируем уникальный slug: title + случайный UUID4 кусок
            base_slug = slugify(self.title)[:20]
            unique_suffix = uuid.uuid4().hex[:8]
            self.slug = f"{base_slug}-{unique_suffix}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.user.email})"
