from rest_framework import serializers
from api.models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

    def create(self, validated_data):
        return super().create(validated_data)