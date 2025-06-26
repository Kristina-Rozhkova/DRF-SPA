from users.apps import UsersConfig
from django.urls import path
from .views import UserListAPIView, UserCreateAPIView, UserDestroyAPIView, UserUpdateAPIView, UserRetrieveAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('', UserListAPIView.as_view(), name='user-list'),
    path('create/', UserCreateAPIView.as_view(), name='user-create'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='user-detail'),
    path('<int:pk>/update/', UserUpdateAPIView.as_view(), name='user-update'),
    path('<int:pk>/delete/', UserDestroyAPIView.as_view(), name='user-delete'),
]