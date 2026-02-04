from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from tasks.models import Task
from tasks.serializers import TaskSerializer

class TaskToggleStatusView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["task"],
        summary="Переключить статус задачи (active ↔ done)",
        description="Переключить статус задачи (active ↔ done)",
        responses=TaskSerializer
    )
    def patch(self, request, slug):
        task = Task.objects.filter(slug=slug, user=request.user).first()

        if not task:
            return Response(
                {"detail": "Not found"},
                status=404
            )

        task.status = Task.Status.DONE if task.status == Task.Status.ACTIVE else Task.Status.ACTIVE
        task.save()
        serializer = TaskSerializer(task)

        return Response(serializer.data)
