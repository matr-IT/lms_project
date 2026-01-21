from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model

from lms.models import Course, Lesson, Subscription
from lms.paginators import MyPagination
from lms.serializers import CourseSerializer, LessonSerializer
from lms.tasks import send_course_update_mail
from users.permissions import IsModerator, IsOwner

User = get_user_model()


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    pagination_class = MyPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            if user.groups.filter(name="moderator").exists():
                return Course.objects.all()
            else:
                return Course.objects.filter(owner=user)
        return Course.objects.none()

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        if course:
            send_course_update_mail.delay(course.pk)

        course.save()

    def get_permissions(self):
        if self.action in ["create"]:
            self.permission_classes = (~IsModerator, IsAuthenticated)
        elif self.action in ["destroy"]:
            self.permission_classes = (~IsModerator | IsOwner,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModerator | IsOwner,)
        elif self.action in ["list"]:
            self.permission_classes = (IsModerator | ~IsOwner,)
        return super().get_permissions()


class SubscriptionAPIView(CreateAPIView):
    serializer_class = CourseSerializer

    def post(self, request, *args, **kwargs):
        user = self.request.user
        course_id = request.data.get("course_id")
        if not course_id:
            return Response({"error": "course_id is required"}, status=400)

        course = get_object_or_404(Course, id=course_id)
        sub = Subscription.objects.filter(user=user, course=course).first()
        if sub:
            sub.delete()
            message = "Unsubscribed successfully."
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Subscribed successfully."
        return Response({"message": message})


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.groups.filter(name="moderator").exists():
                return Lesson.objects.all()
            else:
                return Lesson.objects.filter(owner=user)
        return Lesson.objects.none()

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()

    permission_classes = [IsAuthenticated]


class LessonListAPIView(ListAPIView):
    serializer_class = LessonSerializer
    pagination_class = MyPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            if user.groups.filter(name="moderator").exists():
                return Lesson.objects.all()
            else:
                return Lesson.objects.filter(owner=user)
        return Lesson.objects.none()

    permission_classes = [IsModerator]


class LessonRetrieveAPIView(RetrieveAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            if user.groups.filter(name="moderator").exists():
                return Lesson.objects.all()
            else:
                return Lesson.objects.filter(owner=user)
        return Lesson.objects.none()

    permission_classes = [IsModerator | IsOwner]


class LessonUpdateAPIView(UpdateAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            if user.groups.filter(name="moderator").exists():
                return Lesson.objects.all()
            else:
                return Lesson.objects.filter(owner=user)
        return Lesson.objects.none()

    permission_classes = [IsAuthenticated, IsOwner]


class LessonDestroyAPIView(DestroyAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            return Lesson.objects.filter(owner=user)
        return Lesson.objects.none()

    permission_classes = [IsAuthenticated, IsOwner]
