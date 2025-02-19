from rest_framework.viewsets import ModelViewSet
from api.models.User import User
from api.serializers.User_serializer import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
