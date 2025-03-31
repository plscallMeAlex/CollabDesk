from api.models import TaskState, Task
from api.serializers import TaskStateSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class TaskStateViewSet(ModelViewSet):
    queryset = TaskState.objects.all()
    serializer_class = TaskStateSerializer

    @action(detail=False, methods=["GET"])
    def get_all_states(self, request):
        guild_id = request.query_params.get("guild_id")
        if not guild_id:
            return Response(
                {"error": "Guild is not found"}, status=status.HTTP_400_BAD_REQUEST
            )
        taskstates = TaskState.objects.filter(guild=guild_id)
        serializer = TaskStateSerializer(taskstates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # get all the state in the specific guild
    @action(detail=False, methods=["GET"])
    def in_guild(self, request):
        guild_id = request.query_params.get("guild_id")
        state_id = request.query_params.get("state_id")

        if not guild_id:
            return Response(
                {"error": "Guild is not found"}, status=status.HTTP_400_BAD_REQUEST
            )
        taskstates = TaskState.objects.filter(guild=guild_id)
        # Filter by not equal to state_id
        if state_id:
            taskstates = taskstates.exclude(id=state_id)

        serializer = TaskStateSerializer(taskstates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def create_state(self, request):
        title = request.data.get("title", "").strip()
        guild_id = request.data.get("guild_id")

        # Check if the title already exists
        if TaskState.objects.filter(title__iexact=title, guild_id=guild_id).exists():
            return Response(
                {"error": "State already exists"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Use TaskStateSerializer for validation
        serializer = TaskStateSerializer(data=request.data)
        if serializer.is_valid():
            taskstate = serializer.save()
            return Response(
                TaskStateSerializer(taskstate).data, status=status.HTTP_201_CREATED
            )

    @action(detail=False, methods=["PATCH"])
    def transfer_state(self, request):
        state_id = request.data.get("state_id")
        new_state_id = request.data.get("new_state_id")

        # Check if the state_id and new_state_id are provided
        if not state_id or not new_state_id:
            return Response(
                {"error": "State ID and New State ID are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        task = Task.objects.filter(state=state_id)
        task.update(state=new_state_id)

        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=["DELETE"])
    def delete_state(self, request):
        state_id = request.data.get("state_id")
        TaskState.objects.filter(id=state_id).delete()
        return Response(status=status.HTTP_200_OK)
