from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscription
from materials.paginators import CustomPaginator
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModer, IsOwner


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_summary="Список курсов",
        operation_description="Получение списка всех курсов. Реализована пагинация по 5 объектов на странице. "
        "Максимально - 10 объектов на странице.",
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_summary="Создание курса",
        operation_description="Создание нового курса. Требуются авторизация, запрещено для модераторов.",
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_summary="Просмотр курса",
        operation_description="Просмотр детальной информации о курсе. Требуются права владельца или модератора.",
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_summary="Частичное обновление курса",
        operation_description="Обновление отдельных полей курса. Доступно для модераторов и владельцев.",
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_summary="Редактирование курса",
        operation_description="Редактирование информации о курсе. Требуются права владельца или модератора.",
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_summary="Удаление курса",
        operation_description="Удаление курса из базы данных. При этом удаляются все связанные с курсом уроки. "
        "Требуются права владельца, не доступно для модератора.",
    ),
)
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPaginator

    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        if self.action == "destroy":
            self.permission_classes = (~IsModer | IsOwner,)
        return super().get_permissions()

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        operation_summary="Создание урока",
        operation_description="Создание нового урока. Требуются авторизация, запрещено для модераторов.",
    ),
)
class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModer, IsAuthenticated)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        operation_summary="Список уроков",
        operation_description="Получение списка всех уроков. Требуются авторизация. Реализована пагинация по 5 объектов "
        "на страницу, максимально - 10 уроков на странице.",
    ),
)
class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPaginator


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        operation_summary="Просмотр урока",
        operation_description="Просмотр детальной информации об уроке. Требуются авторизация, также доступно для "
        "модераторов и владельцев.",
    ),
)
class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsModer | IsOwner,
    )


@method_decorator(
    name="patch",
    decorator=swagger_auto_schema(
        operation_summary="Частичное редактирование урока",
        operation_description="Частичное редактирование информации об уроке. Требуются авторизация, также доступно для "
        "модераторов и владельцев.",
    ),
)
@method_decorator(
    name="put",
    decorator=swagger_auto_schema(
        operation_summary="Редактирование урока",
        operation_description="Редактирование информации об уроке. Требуются авторизация, также доступно для "
        "модераторов и владельцев.",
    ),
)
class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsModer | IsOwner,
    )


@method_decorator(
    name="delete",
    decorator=swagger_auto_schema(
        operation_summary="Удаление урока",
        operation_description="Удаление урока из базы данных. Требуются авторизация, также доступно для "
        "владельцев, но не доступно для модераторов.",
    ),
)
class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = (
        IsAuthenticated,
        ~IsModer | IsOwner,
    )


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        operation_summary="Подписка на курс",
        operation_description="Добавление курса в избранное, чтобы получать уведомления об обновлении курса. "
        "Требуются авторизация. При успешном запросе выводит информацию о статусе подписки.",
    ),
)
class SubscriptionAPIView(APIView):
    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course_id")
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена"
        return Response({"message": message})
