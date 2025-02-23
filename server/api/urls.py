from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.User_view import UserViewSet
from api.views.Task_view import TaskViewSet
from api.views.Role_view import RoleViewSet
from api.viewss import home

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")  # ip/users
router.register(r"tasks", TaskViewSet, basename="tasks")  # ip/tasks
router.register(r"roles", RoleViewSet, basename="roles")  # ip/roles


urlpatterns = [
    path("", home, name="home"),
    path("", include(router.urls)),
]
