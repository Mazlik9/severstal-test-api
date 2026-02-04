import pytest

from django.contrib.auth import get_user_model
from tasks.models import Task
from tasks.serializers import TaskSerializer

User = get_user_model()


@pytest.mark.django_db
class TestTaskSerializer:

    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            email="serializer@example.com",
            password="password123",
            full_name="Serializer User",
        )

    def test_serializer_valid_data(self, user):
        """
        Сериализатор валиден при корректных данных
        """
        data = {
            "title": "Test task",
            "description": "Test description",
            "status": Task.Status.ACTIVE,
        }

        serializer = TaskSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

    def test_serializer_creates_task(self, user):
        """
        Сериализатор корректно создаёт задачу
        """
        data = {
            "title": "Created task",
            "description": "Created via serializer",
            "status": Task.Status.DONE,
        }

        serializer = TaskSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        task = serializer.save(user=user)

        assert task.pk is not None
        assert task.user == user
        assert task.title == data["title"]
        assert task.description == data["description"]
        assert task.status == Task.Status.DONE
        assert task.slug is not None

    def test_read_only_fields_are_ignored(self, user):
        """
        read_only поля не должны устанавливаться из входных данных
        """
        data = {
            "slug": "fake-slug",
            "user": user.id,
            "title": "Readonly test",
            "description": "Readonly fields",
            "status": Task.Status.ACTIVE,
        }

        serializer = TaskSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        task = serializer.save(user=user)

        assert task.slug != "fake-slug"

        assert task.user == user

    def test_serializer_representation(self, user):
        """
        Проверка serializer.data
        """
        task = Task.objects.create(
            user=user,
            title="Serialized task",
            description="Serializer output",
            status=Task.Status.ACTIVE,
        )

        serializer = TaskSerializer(task)
        data = serializer.data

        assert data["slug"] == task.slug
        assert data["title"] == task.title
        assert data["description"] == task.description
        assert data["status"] == task.status
        assert data["user"] == user.id
        assert "created_at" in data
        assert "updated_at" in data
