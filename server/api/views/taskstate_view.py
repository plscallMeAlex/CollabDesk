from api.models import TaskState
from api.serializers.taskstate_serializer import TaskStateSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class TaskStateViewSet(ModelViewSet):
    queryset = TaskState.objects.all()
    serializer_class = TaskStateSerializer

    # get all the state in the specific guild
    @action(detail=False, methods=["GET"])
    def in_guild(self, request):
        guild_id = request.query_params.get("guild_id")
        taskstates = TaskState.objects.filter(guild_id=guild_id)
        serializer = TaskStateSerializer(taskstates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
