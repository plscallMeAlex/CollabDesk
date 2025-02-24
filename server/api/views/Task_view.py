from api.models.task import Task
from api.models.guild import Guild
from api.models.user import User
from api.serializers.Task_serializer import TaskSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    # get all tasks in a guild
    @action(detail=False, methods=["GET"])
    def in_guild(self, request): 
        guild_id = request.query_params.get("guild_id")
        guild = Guild.objects.filter(id=guild_id).first()
        if guild is None:
            return Response(
                {"error": "Guild not found"},
                status=status.HTTP_404_NOT_FOUND
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
                {"error": "Guild not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        assigner = User.objects.filter(id=assigner_id).first()
        if assigner is None:
            return Response(
                {"error": "Assigner not found"},
                status=status.HTTP_404_NOT_FOUND
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
                {"error": "Guild not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        assignee = User.objects.filter(id=assignee_id).first()
        if assignee is None:
            return Response(
                {"error": "Assignee not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        tasks = Task.objects.filter(guild=guild, assignee=assignee)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    