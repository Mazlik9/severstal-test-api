from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from drf_spectacular.utils import extend_schema
from tasks.models import Task
from tasks.serializers import TaskSerializer

class TaskListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["task"],
        summary="Список задач текущего пользователя",
        description="Список задач текущего пользователя. Можно фильтровать по статусу и искать по заголовку/описанию.",
        responses=TaskSerializer(many=True)
    )
    def get(self, request):
        queryset = Task.objects.filter(user=request.user)

        status_param = request.query_params.get('status')
        if status_param in ['active', 'done']:
            queryset = queryset.filter(status=status_param)

        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )

        paginator = PageNumberPagination()
        paginator.page_size = 10
        page = paginator.paginate_queryset(queryset, request)
        serializer = TaskSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        tags=["task"],
        summary="Создать новую задачу",
        description="Создать новую задачу",
        request=TaskSerializer,
        responses=TaskSerializer
    )
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
