from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Pay, User
from .permissions import IsModer, IsOwner
from .serializers import (PaySerializer, UserDetailSerializer,
                          UserPublicSerializer, UserSerializer)
from .services import (check_payment_status, converter, create_stripe_price,
                       create_stripe_sessions)


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        operation_summary="Создание пользователя",
        operation_description="Создание нового пользователя. Для авторизации требуются email и пароль.",
    ),
)
class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        operation_summary="Список пользователей",
        operation_description="Вывод списка авторизованных пользователей. Требуется авторизация. Для просмотра доступны "
        "поля: email, имя, город, аватар.",
        responses={200: UserPublicSerializer(many=True)},
    ),
)
class UserListAPIView(ListAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        user = self.request.user

        if user.is_authenticated:
            return UserPublicSerializer
        raise PermissionDenied


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        operation_summary="Просмотр профиля",
        operation_description="Просмотр профиля пользователя. Требуется авторизация. Для владельца профиля и администратора"
        " для просмотра доступны поля: email, имя, фамилия, телефон, город, аватар, история платежей."
        " Для других пользователей на просмотр доступны поля: email, имя, город, аватар.",
        responses={
            200: openapi.Response(
                description="Успешный ответ",
                examples={
                    "application/json": {
                        "Для владельца/админа": UserDetailSerializer().data,
                        "Для других": {
                            "email": "",
                            "first_name": "",
                            "city": "",
                            "avatar": "",
                        },
                    }
                },
            )
        },
    ),
)
class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        user = self.request.user
        requested_user = self.get_object()

        if user.is_staff or user.is_superuser or user.id == requested_user.id:
            return UserDetailSerializer
        return UserPublicSerializer


@method_decorator(
    name="put",
    decorator=swagger_auto_schema(
        operation_summary="Редактирование профиля",
        operation_description="Редактирование полей профиля пользователя. Требуется авторизация. Для владельца профиля и "
        "администратора для редактирования доступны поля: email, имя, фамилия, телефон, город, "
        "аватар, история платежей.",
        responses={200: UserDetailSerializer(many=True)},
    ),
)
@method_decorator(
    name="patch",
    decorator=swagger_auto_schema(
        operation_summary="Частичное редактирование профиля",
        operation_description="Обновление отдельных полей профиля пользователя. Требуется авторизация. Для владельца "
        "профиля и администратора для обновления доступны поля: email, имя, фамилия, телефон, город, "
        "аватар, история платежей.",
        responses={200: UserDetailSerializer(many=True)},
    ),
)
class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        user = self.request.user
        requested_user = self.get_object()

        if user.is_staff or user.is_superuser or user.id == requested_user.id:
            return UserDetailSerializer
        raise PermissionDenied


@method_decorator(
    name="delete",
    decorator=swagger_auto_schema(
        operation_summary="Удаление пользователя",
        operation_description="Удаление пользователя из базы данных. Доступно только для владельца профиля.",
    ),
)
class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_summary="Список платежей",
        operation_description="Получение списка всех платежей пользователя. Реализована фильтрация по урокам, курсам, "
        "способам оплаты. Доступно для владельцев профиля и администратора.",
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_summary="Создание платежа",
        operation_description="Создание нового платежа за курс или отдельный урок.",
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_summary="Просмотр платежа",
        operation_description="Просмотр детальной информации о платеже. Требуются права владельца профиля или "
        "администратора.",
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_summary="Частичное обновление платежа",
        operation_description="Обновление отдельных полей платежа. Требуются права администратора.",
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_summary="Редактирование платежа",
        operation_description="Редактирование информации о платеже. Требуются права администратора.",
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_summary="Удаление платежа",
        operation_description="Удаление платежа из базы данных. Требуются права администратора.",
    ),
)
@method_decorator(
    name="check_status",
    decorator=swagger_auto_schema(
        operation_summary="Проверка статуса оплаты",
        operation_description="Проверяет текущий статус платежа в системе stripe.",
        responses={
            200: openapi.Response(
                description="Статус платежа",
                examples={
                    "application/json": {
                        "payment_id": 1,
                        "status": "paid",
                        "details": {
                            "status": "complete",
                            "payment_status": "paid",
                            "user_email": "user@example.com",
                            "payment_method": "Перевод",
                        },
                    }
                },
            ),
            400: "Неверный ID платежа.",
        },
    ),
)
class PayViewSet(ModelViewSet):
    queryset = Pay.objects.all()
    serializer_class = PaySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("lesson", "course", "form_of_payment")
    ordering_fields = ("payment_date",)

    def get_permissions(self):
        if self.action in ["create", "retrieve"]:
            self.permission_classes = (IsOwner | IsAdminUser,)
        elif self.action in ["update", "destroy"]:
            self.permission_classes = (IsAdminUser,)
        return super().get_permissions()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        amount_in_dollars = converter(payment.amount)
        price = create_stripe_price(amount_in_dollars)
        session_id, payment_link = create_stripe_sessions(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()

    @action(detail=True, methods=["get"])
    def check_status(self, request, pk=None):
        """Проверка статуса оплаты."""
        payment = self.get_object()
        if not payment.session_id:
            return Response({"error": "Неверный ID платежа."}, status=400)

        status_info = check_payment_status(payment.session_id)
        payment.payment_status = status_info.get(
            "payment_status", payment.payment_status
        )
        payment.save()

        return Response(
            {
                "payment_id": payment.id,
                "status": payment.payment_status,
                "details": status_info,
            }
        )
