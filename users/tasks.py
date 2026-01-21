from celery import shared_task

from django.utils import timezone
from datetime import timedelta
from .models import User


@shared_task
def check_activity():

    check_date = timezone.now() - timedelta(days=30)

    inactive_users = User.objects.filter(last_login__lt=check_date)

    for user in inactive_users:
        user.is_active = False
        user.save()
