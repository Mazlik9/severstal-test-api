from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_spectacular.utils import extend_schema
from tasks.models import Task
from tasks.serializers import TaskSerializer

class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, slug, user):
        try:
            return Task.objects.get(slug=slug, user=user)
        except Task.DoesNotExist:
            return None

    @extend_schema(
        tags=["task"],
        summary="Получить задачу по slug",
        description="Получить задачу по slug",
        responses=TaskSerializer
    )
    def get(self, request, slug):
        task = self.get_object(slug, request.user)
        if not task:
            return Response(
                {"detail": "Not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    @extend_schema(
        tags=["task"],
        summary="Частично обновить задачу",
        description="Частично обновить задачу",
        request=TaskSerializer,
        responses=TaskSerializer
    )
    def patch(self, request, slug):
        task = self.get_object(slug, request.user)

        if not task:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    @extend_schema(
        tags=["task"],
        summary="Удалить задачу",
        description="Удалить задачу",
    )
    def delete(self, request, slug):
        task = self.get_object(slug, request.user)

        if not task:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        task.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
