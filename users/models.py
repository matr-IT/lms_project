from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CASCADE

from lms.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Введите номер телефона",
    )
    city = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Введите Ваш город",
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        blank=True,
        null=True,
        verbose_name="Фото профиля",
        help_text="Загрузите фото для Вашего профиля",
    )

    token = models.CharField(
        max_length=100, verbose_name="токен", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):

    PAYMENT_CHOICES = (("cash", "наличные"), ("transaction", "перевод на счет"))

    user = models.ForeignKey(User, on_delete=CASCADE, verbose_name="Плательщик")

    payment_date = models.DateTimeField(verbose_name="дата оплаты", auto_now_add=True)

    paid_course = models.ForeignKey(
        Course, on_delete=CASCADE, verbose_name="Оплаченный курс", blank=True, null=True
    )

    paid_lesson = models.ForeignKey(
        Lesson, on_delete=CASCADE, verbose_name="Оплаченный урок", blank=True, null=True
    )

    payment_sum = models.IntegerField(
        verbose_name="Сумма оплаты", help_text="Введите сумму оплаты"
    )

    payment_type = models.CharField(verbose_name="Тип платежа", choices=PAYMENT_CHOICES)
