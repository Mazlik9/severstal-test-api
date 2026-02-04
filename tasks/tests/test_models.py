import pytest
from tasks.models import Task
from users.models import User

@pytest.fixture
def user(db):
    """Создаем тестового пользователя."""
    return User.objects.create_user(
        email="struser@example.com",
        password="password123",
        full_name="Test User"
    )

@pytest.mark.django_db
class TestTaskModel:

    def test_create_task(self, user):
        """Проверка создания задачи"""
        task = Task.objects.create(
            user=user,
            title="String Task",
            description="Description for task"
        )

        assert task.pk is not None
        assert task.user == user
        assert task.title == "String Task"
        assert task.status == Task.Status.ACTIVE
        assert task.slug is not None
        assert len(task.slug) > 0

    def test_task_str_representation(self, user):
        task = Task.objects.create(
            user=user,
            title="String Task"
        )

        expected = f"{task.title} ({user.email})"
        assert str(task) == expected
