from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson, Subscription

from .validators import LinkVideoValidator


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [LinkVideoValidator(field="video")]


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    count_lessons = SerializerMethodField()
    lessons = LessonSerializer(many=True, source="lesson_set", read_only=True)
    is_subscribed = SerializerMethodField()

    def get_count_lessons(self, course):
        return Lesson.objects.filter(course=course.pk).count()

    def get_is_subscribed(self, course):
        user = self.context.get("request").user

        return Subscription.objects.filter(user=user, course=course).exists()

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "preview",
            "description",
            "count_lessons",
            "lessons",
            "is_subscribed",
        )
