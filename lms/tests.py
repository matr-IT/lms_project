from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from rest_framework import status

from lms.models import Course, Lesson, Subscription
from django.contrib.auth.models import Group

User = get_user_model()


class LessonsAndSubscriptionTests(APITestCase):
    def setUp(self):
        self.moderator_group, _ = Group.objects.get_or_create(name="moderators")
        self.moderator_group_alt, _ = Group.objects.get_or_create(name="moderator")

        self.moderator = User(email="mod@example.com")
        self.moderator.set_password("modpass")
        self.moderator.save()
        self.moderator.groups.add(self.moderator_group)
        self.moderator.groups.add(self.moderator_group_alt)

        self.owner = User(email="owner@example.com")
        self.owner.set_password("ownerpass")
        self.owner.save()

        self.other = User(email="other@example.com")
        self.other.set_password("otherpass")
        self.other.save()

        self.course = Course.objects.create(
            name="Test Course", description="Desc", owner=self.owner
        )

        self.lesson1 = Lesson.objects.create(
            name="Lesson 1", description="L1", course=self.course, owner=self.owner
        )
        self.lesson2 = Lesson.objects.create(
            name="Lesson 2", description="L2", course=self.course, owner=self.other
        )

        self.client = APIClient()

    def test_list_lessons_as_moderator(self):
        self.client.force_authenticate(user=self.moderator)
        url = reverse("lms:lessons_list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(resp.data["results"]), 2)

    def test_list_lessons_as_owner(self):
        self.client.force_authenticate(user=self.owner)
        url = reverse("lms:lessons_list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_lesson_permission(self):
        url = reverse("lms:lessons_retrieve", kwargs={"pk": self.lesson2.id})
        self.client.force_authenticate(user=self.owner)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.client.force_authenticate(user=self.moderator)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_lesson(self):
        url = reverse("lms:lessons_create")
        data = {
            "name": "New Lesson",
            "description": "New",
            "course": self.course.id,
            "url": "https://www.youtube.com/watch?v=abc123",
        }
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(user=self.owner)
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.filter(name="New Lesson").exists(), True)

    def test_update_lesson(self):
        url = reverse("lms:lessons_update", kwargs={"pk": self.lesson1.id})
        data = {"name": "Updated Name"}
        self.client.force_authenticate(user=self.other)
        resp = self.client.patch(url, data)
        self.assertIn(
            resp.status_code, (status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND)
        )
        self.client.force_authenticate(user=self.owner)
        resp = self.client.patch(url, data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.lesson1.refresh_from_db()
        self.assertEqual(self.lesson1.name, "Updated Name")

    def test_delete_lesson(self):
        url = reverse("lms:lessons_delete", kwargs={"pk": self.lesson1.id})
        self.client.force_authenticate(user=self.other)
        resp = self.client.delete(url)
        self.assertIn(
            resp.status_code, (status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND)
        )
        self.client.force_authenticate(user=self.owner)
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson1.id).exists())

    def test_subscription_toggle(self):
        url = reverse("lms:subscribe")
        data = {"course_id": self.course.id}
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(user=self.other)
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(
            Subscription.objects.filter(user=self.other, course=self.course).exists()
        )
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertFalse(
            Subscription.objects.filter(user=self.other, course=self.course).exists()
        )
