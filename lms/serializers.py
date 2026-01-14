from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from lms.models import Course, Lesson
from lms.validators import validate_url


class CourseSerializer(ModelSerializer):

    count_of_lessons = serializers.SerializerMethodField()
    subscription = serializers.SerializerMethodField()

    def get_count_of_lessons(self, course):
        return Lesson.objects.filter(course=course).count()

    lessons = serializers.SerializerMethodField()

    def get_lessons(self, course):
        all_lessons_of_course = Lesson.objects.filter(course=course).all()
        lessons = []
        for lesson in all_lessons_of_course:
            lessons.append(str(lesson))
        return lessons

    def get_subscription(self, course):
        request = None
        if isinstance(self.context, dict):
            request = self.context.get("request")
        user = getattr(request, "user", None)
        if user and getattr(user, "is_authenticated", False):
            return course.subscriptions.filter(user=user).exists()
        return False

    class Meta:
        model = Course
        fields = ("name", "count_of_lessons", "lessons", "subscription")


class LessonSerializer(ModelSerializer):

    url = serializers.URLField(
        validators=[
            validate_url,
        ]
    )

    class Meta:
        model = Lesson
        fields = "__all__"
        read_only_fields = ("owner",)
