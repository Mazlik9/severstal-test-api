from rest_framework import serializers
from tasks.models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'slug',
            'user',
            'title',
            'description',
            'status',
            'created_at',
            'updated_at'
        ]
        
        read_only_fields = [
            'slug',
            'user',
            'created_at',
            'updated_at'
        ]
