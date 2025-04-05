from rest_framework import serializers
from api.models import TaskState


class TaskStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskState
        fields = "__all__"

    def create(self, validated_data):
        return super().create(validated_data)
