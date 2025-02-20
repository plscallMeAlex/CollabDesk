from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.User_view import UserViewSet
from api.viewss import home

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")  # ip/users

urlpatterns = [
    path("", home, name="home"),
    path("", include(router.urls)),
]
