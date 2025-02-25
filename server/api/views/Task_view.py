from api.models import Task
from api.models import Guild
from api.models import User
from api.serializers.task_serializer import TaskSerializer, TaskCreateSerializer
from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    # create a task
    @action(detail=False, methods=["POST"])
    def create_task(self, request):
        title = request.data.get("title", "").strip()

        # Check if the title already exists
        if Task.objects.filter(title__iexact=title).exists():
            return Response(
                {"error": "Task already exists"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Use TaskCreateSerializer for validation
        serializer = TaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            return Response(
                TaskCreateSerializer(task).data, status=status.HTTP_201_CREATED
            )

        # Return validation errors if serializer is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # get all tasks in a guild
    @action(detail=False, methods=["GET"])
    def in_guild(self, request):
        guild_id = request.query_params.get("guild_id")
        guild = Guild.objects.filter(id=guild_id).first()
        if guild is None:
            return Response(
                {"error": "Guild not found"}, status=status.HTTP_404_NOT_FOUND
            )
        tasks = Task.objects.filter(guild=guild)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # get all tasks in a guild assigned by a user
    @action(detail=False, methods=["GET"])
    def in_guild_by_assigner(self, request):
        guild_id = request.query_params.get("guild_id")
        assigner_id = request.query_params.get("assigner_id")
        guild = Guild.objects.filter(id=guild_id).first()
        if guild is None:
            return Response(
                {"error": "Guild not found"}, status=status.HTTP_404_NOT_FOUND
            )
        assigner = User.objects.filter(id=assigner_id).first()
        if assigner is None:
            return Response(
                {"error": "Assigner not found"}, status=status.HTTP_404_NOT_FOUND
            )
        tasks = Task.objects.filter(guild=guild, assigner=assigner)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # get all tasks in a guild assigned to a user
    @action(detail=False, methods=["GET"])
    def in_guild_by_assignee(self, request):
        guild_id = request.query_params.get("guild_id")
        assignee_id = request.query_params.get("assignee_id")
        guild = Guild.objects.filter(id=guild_id).first()
        if guild is None:
            return Response(
                {"error": "Guild not found"}, status=status.HTTP_404_NOT_FOUND
            )
        assignee = User.objects.filter(id=assignee_id).first()
        if assignee is None:
            return Response(
                {"error": "Assignee not found"}, status=status.HTTP_404_NOT_FOUND
            )
        tasks = Task.objects.filter(guild=guild, assignee=assignee)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # get all tasks in a guild with a specific state
    @action(detail=False, methods=["GET"])
    def in_guild_by_state(self, request):
        state_id = request.query_params.get("state_id")
        tasks = Task.objects.filter(state=state_id)
        if tasks is None:
            return Response(
                {"error": "Tasks not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
