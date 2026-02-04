from django.urls import path
from tasks.views import TaskListCreateView, TaskDetailView, TaskToggleStatusView

urlpatterns = [
    path('', TaskListCreateView.as_view(), name='task-list-create'),
    path('<slug:slug>/', TaskDetailView.as_view(), name='task-detail'),
    path('<slug:slug>/toggle-status/', TaskToggleStatusView.as_view(), name='task-toggle-status'),
]
