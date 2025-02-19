from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.User_view import UserViewSet
from api.viewss import home, register, login

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("", include(router.urls)),
]
