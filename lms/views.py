from django.template.context_processors import request
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model

from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner

User = get_user_model()


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer

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

    permission_classes = [IsAuthenticated, ~IsModerator]


class LessonListAPIView(ListAPIView):
    serializer_class = LessonSerializer

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

    permission_classes = [IsModerator | IsOwner]


class LessonDestroyAPIView(DestroyAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            return Lesson.objects.filter(owner=user)
        return Lesson.objects.none()

    permission_classes = [~IsModerator, IsOwner]
