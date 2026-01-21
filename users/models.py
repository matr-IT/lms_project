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

    last_login = models.DateTimeField(
        verbose_name="Последний вход", auto_now=True, null=True, blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):

    user = models.ForeignKey(User, on_delete=CASCADE, verbose_name="Плательщик")
    payment_date = models.DateTimeField(verbose_name="дата оплаты", auto_now_add=True)
    paid_course = models.ForeignKey(
        Course, on_delete=CASCADE, verbose_name="Оплаченный курс", blank=True, null=True
    )
    paid_lesson = models.ForeignKey(
        Lesson, on_delete=CASCADE, verbose_name="Оплаченный урок", blank=True, null=True
    )
    payment_sum = models.PositiveIntegerField(
        verbose_name="Сумма оплаты", help_text="Введите сумму оплаты"
    )
    link = models.URLField(
        verbose_name="Ссылка на оплату",
        help_text="Введите ссылку на оплату",
        blank=True,
        null=True,
    )
    session_id = models.CharField(
        max_length=200,
        verbose_name="ID сессии",
        help_text="Введите ID сессии",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"Платеж {self.pk} пользователя {self.user.email}"
