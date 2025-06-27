from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    count_lessons = SerializerMethodField()
    lessons = LessonSerializer(many=True, source='lesson_set')

    
    def get_count_lessons(self, course):
        return Lesson.objects.filter(course=course.pk).count()
    
    class Meta:
        model = Course
        fields = ('name', 'preview', 'description', 'count_lessons', 'lessons')
