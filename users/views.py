from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.viewsets import ModelViewSet
from .models import User, Pay
from .serializers import UserSerializer, PaySerializer, UserListSerializer, UserPublicSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import AllowAny


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()

    def get_serializer_class(self):
        user = self.request.user
        if user.id == self.queryset.get(id=user.id):
            return UserListSerializer
        return UserPublicSerializer


class UserRetrieveAPIView(LoginRequiredMixin, RetrieveAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        user = self.request.user
        if user.is_staff or user.is_superuser or user.id == self.queryset.get(id=user.id):
            return UserListSerializer
        return PermissionDenied


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_serializer_class(self):
        user = self.request.user

        if user.is_staff or user.is_superuser or user.id == self.queryset.get(id=user.id):
            return UserListSerializer
        return PermissionDenied


class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()


class PayViewSet(ModelViewSet):
    queryset = Pay.objects.all()
    serializer_class = PaySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ('lesson', 'course', 'form_of_payment')
    ordering_fields = ('payment_date',)
