from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.viewsets import ModelViewSet
from .models import User, Pay
from .serializers import UserSerializers, PaySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


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


class PayViewSet(ModelViewSet):
    queryset = Pay.objects.all()
    serializer_class = PaySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ('lesson', 'course', 'form_of_payment')
    ordering_fields = ('payment_date',)

