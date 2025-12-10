from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from lms.models import Course, Lesson


class CourseSerializer(ModelSerializer):

    count_of_lessons = SerializerMethodField()

    def get_count_of_lessons(self, course):
        return Lesson.objects.filter(course=course).count()

    lessons = SerializerMethodField()

    def get_lessons(self, course):
        all_lessons_of_course = Lesson.objects.filter(course=course).all()
        lessons = []
        for lesson in all_lessons_of_course:
            lessons.append(str(lesson))
        return lessons

    class Meta:
        model = Course
        fields = ("name", "count_of_lessons", "lessons")


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


