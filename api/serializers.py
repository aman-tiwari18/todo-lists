from rest_framework.serializers import ModelSerializer
from .models import *


class TodoListSerializer(ModelSerializer):
    class Meta:
        model = TodoList
        fields = "__all__"

    def update(self, instance, validated_data):
        validated_data.pop("account", None)
        return super().update(instance, validated_data)


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

    def update(self, instance, validated_data):
        validated_data.pop("todoList", None)
        return super().update(instance, validated_data)
