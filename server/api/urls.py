from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.view import home
from api.views.user_view import UserViewSet


router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")  # ip/users

urlpatterns = [
    path("", home, name="home"),
    path("", include(router.urls)),
]
