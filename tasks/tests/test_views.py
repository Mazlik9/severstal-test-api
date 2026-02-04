import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from tasks.models import Task

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(
        email="viewuser@example.com",
        password="password123",
        full_name="View User",
    )

@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def task(user):
    return Task.objects.create(
        user=user,
        title="Test task",
        description="Test description",
        status=Task.Status.ACTIVE,
    )

@pytest.mark.django_db
class TestTaskListCreateView:

    def test_get_task_list(self, auth_client, task):
        url = reverse("task-list-create")

        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK

        assert response.data["count"] == 1
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["title"] == task.title

    def test_create_task(self, auth_client):
        url = reverse("task-list-create")

        payload = {
            "title": "New task",
            "description": "Created via API",
            "status": Task.Status.ACTIVE,
        }

        response = auth_client.post(url, payload, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert Task.objects.count() == 1
        assert Task.objects.first().title == payload["title"]

@pytest.mark.django_db
class TestTaskDetailView:

    def test_get_task_list(self, auth_client, task):
        url = reverse("task-list-create")

        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["title"] == task.title

    def test_delete_task(self, auth_client, task):
        url = reverse("task-detail", kwargs={"slug": task.slug})

        response = auth_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Task.objects.count() == 0

    def test_user_cannot_access_foreign_task(self, auth_client):
        other_user = User.objects.create_user(
            email="other@example.com",
            password="password123",
            full_name="Other User",
        )

        foreign_task = Task.objects.create(
            user=other_user,
            title="Foreign task",
        )

        url = reverse("task-detail", kwargs={"slug": foreign_task.slug})
        response = auth_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
class TestTaskToggleStatusView:

    def test_toggle_task_status(self, auth_client, task):
        url = reverse("task-toggle-status", kwargs={"slug": task.slug})

        response = auth_client.patch(url)

        assert response.status_code == status.HTTP_200_OK

        task.refresh_from_db()
        assert task.status == Task.Status.DONE

    def test_toggle_twice(self, auth_client, task):
        url = reverse("task-toggle-status", kwargs={"slug": task.slug})

        auth_client.patch(url)
        auth_client.patch(url)

        task.refresh_from_db()
        assert task.status == Task.Status.ACTIVE

@pytest.mark.django_db
def test_unauthorized_access(api_client):
    url = reverse("task-list-create")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED