from django.urls import path
from rest_framework.routers import SimpleRouter
from users.apps import UsersConfig
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (UserCreateAPIView, UserDestroyAPIView, UserListAPIView,
                    UserRetrieveAPIView, UserUpdateAPIView, PayViewSet)
from rest_framework.permissions import AllowAny

app_name = UsersConfig.name

router = SimpleRouter()
router.register(r"pay", PayViewSet, basename="pay")

urlpatterns = [
    path("", UserListAPIView.as_view(), name="user-list"),
    path("create/", UserCreateAPIView.as_view(), name="user-create"),
    path("<int:pk>/", UserRetrieveAPIView.as_view(), name="user-detail"),
    path("<int:pk>/update/", UserUpdateAPIView.as_view(), name="user-update"),
    path("<int:pk>/delete/", UserDestroyAPIView.as_view(), name="user-delete"),

    path('token/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
] + router.urls
