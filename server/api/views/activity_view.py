from api.models import Activity
from api.serializers.activity_serializer import AcitvitySerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class ActivityViewSet(ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = AcitvitySerializer

    @action(detail=False, methods=["POST"])
    def create_activity(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        pass

    @action(detail=False, methods=["GET"])
    def get_all_activity_by_guild(self, request):
        guild_id = request.query_params.get("guild_id")
        if guild_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        activities = Activity.objects.filter(guild=guild_id)
        if not activities.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AcitvitySerializer(activities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
