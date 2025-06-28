from django.urls import path
from rest_framework.routers import SimpleRouter
from users.apps import UsersConfig

from .views import (UserCreateAPIView, UserDestroyAPIView, UserListAPIView,
                    UserRetrieveAPIView, UserUpdateAPIView, PayViewSet)

app_name = UsersConfig.name

router = SimpleRouter()
router.register(r"pay", PayViewSet, basename="pay")

urlpatterns = [
    path("", UserListAPIView.as_view(), name="user-list"),
    path("create/", UserCreateAPIView.as_view(), name="user-create"),
    path("<int:pk>/", UserRetrieveAPIView.as_view(), name="user-detail"),
    path("<int:pk>/update/", UserUpdateAPIView.as_view(), name="user-update"),
    path("<int:pk>/delete/", UserDestroyAPIView.as_view(), name="user-delete"),
] + router.urls
