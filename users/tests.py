from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from unittest.mock import patch
from rest_framework import status

from users.models import Payment
from lms.models import Course

User = get_user_model()


class PaymentsTests(APITestCase):
    def setUp(self):
        self.user = User(email="payuser@example.com")
        self.user.set_password("testpass")
        self.user.save()
        self.client = APIClient()
        self.course = Course.objects.create(name="PayCourse")

    @patch("users.views.create_stripe_price")
    @patch("users.views.create_stripe_checkout_session")
    def test_create_payment_triggers_stripe(self, mock_checkout, mock_price):
        mock_price.return_value = {"id": "price_123"}
        mock_checkout.return_value = ("sess_123", "https://checkout.example/sess_123")

        self.client.force_authenticate(user=self.user)
        url = reverse("users:payments-list")
        data = {"payment_sum": 100, "paid_course": self.course.id}
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Payment.objects.filter(user=self.user, payment_sum=100).exists()
        )
        payment = Payment.objects.get(user=self.user, payment_sum=100)
        self.assertEqual(payment.session_id, "sess_123")
        self.assertEqual(payment.link, "https://checkout.example/sess_123")
