from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.task_view import TaskViewSet
from api.views.taskstate_view import TaskStateViewSet
from api.views.role_view import RoleViewSet
from api.views.user_view import UserViewSet
from api.views.announcement_view import AnnouncementViewSet
from api.views.view import home


router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")  # ip/users
router.register(r"tasks", TaskViewSet, basename="tasks")  # ip/tasks
router.register(r"roles", RoleViewSet, basename="roles")  # ip/roles
router.register(r"taskstates", TaskStateViewSet, basename="taskstates")  # ip/taskstates
router.register(r"announcements", AnnouncementViewSet, basename="announcements")  # ip/announcements

urlpatterns = [
    path("", home, name="home"),
    path("", include(router.urls)),
]
