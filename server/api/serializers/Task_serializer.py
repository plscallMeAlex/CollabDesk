from rest_framework import serializers
from api.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

    def create(self, validated_data):
        return super().create(validated_data)


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["title", "state", "assigner"]

    def create(self, validated_data):
        state = validated_data["state"]
        guild = state.guild if hasattr(state, "guild") else None

        task = Task.objects.create(
            title=validated_data["title"],
            assigner=validated_data["assigner"],
            state=state,
            guild=guild,
            assignee=None,
            due_date=None,
            announce_date=None,
            description="",
        )

        return task
