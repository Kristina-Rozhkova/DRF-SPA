from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from .models import Pay, User
from .serializers import (PaySerializer, UserDetailSerializer,
                          UserPublicSerializer, UserSerializer)


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        user = self.request.user

        if user.is_authenticated:
            return UserPublicSerializer
        raise PermissionDenied


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        user = self.request.user
        requested_user = self.get_object()

        if user.is_staff or user.is_superuser or user.id == requested_user.id:
            return UserDetailSerializer
        return UserPublicSerializer


class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        user = self.request.user
        requested_user = self.get_object()

        if user.is_staff or user.is_superuser or user.id == requested_user.id:
            return UserDetailSerializer
        raise PermissionDenied


class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()


class PayViewSet(ModelViewSet):
    queryset = Pay.objects.all()
    serializer_class = PaySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("lesson", "course", "form_of_payment")
    ordering_fields = ("payment_date",)
