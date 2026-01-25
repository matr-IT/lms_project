from celery import shared_task
import logging

from lms.models import Course, Subscription

logger = logging.getLogger(__name__)


@shared_task(bind=True, default_retry_delay=60, max_retries=3)
def send_course_update_mail(self, course_pk):
    course = Course.objects.get(pk=course_pk)
    subscriptions = Subscription.objects.select_related("user").filter(course=course)
    for sub in subscriptions:
        user = sub.user
        try:
            user.email_user(
                subject=f"Обновление в курсе: {course.name}",
                message=(
                    f"В курсе {course.name} произошло обновление. "
                    "Посетите курс для получения дополнительной информации."
                ),
            )
        except Exception as e:
            print("Ошибка при отправке email:", e)
