from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from users.models import Payment, User

from users.serializers import PaymentSerializer, UserSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentViewSet(ModelViewSet):
    def get_queryset(self):
        return Payment.objects.all()
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["course", "lesson", "payment_type"]
    ordering_fields = ["payment_date"]

