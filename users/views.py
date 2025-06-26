from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.exceptions import PermissionDenied
from .models import User
from .serializers import UserSerializers
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializers
    queryset = User.objects.all()


class UserListAPIView(ListAPIView):
    serializer_class = UserSerializers
    queryset = User.objects.all()


class UserRetrieveAPIView(LoginRequiredMixin, RetrieveAPIView):
    serializer_class = UserSerializers
    queryset = User.objects.all()

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return self.queryset
        else:
            raise PermissionDenied


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserSerializers
    queryset = User.objects.all()


class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()
