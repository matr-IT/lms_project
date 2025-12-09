from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from lms.models import Course, Lesson


class CourseSerializer(ModelSerializer):

    count_of_lessons = SerializerMethodField()

    def get_count_of_lessons(self, course):
        return Lesson.objects.filter(course=course).count()


    class Meta:
        model = Course
        fields = ("name", "count_of_lessons")

class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"

