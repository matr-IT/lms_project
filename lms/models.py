from django.db import models
from django.db.models import CASCADE


class Course(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название курса",
        help_text="Укажите название курса",
    )
    preview = models.ImageField(
        upload_to="courses/image",
        help_text="Добавьте заставку для курса",
        blank=True,
        null=True,
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="описание курса",
        help_text="Добавьте описание",
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=CASCADE,
        null=True,
        blank=True,
        verbose_name="Владелец",
        help_text="Владелец курса",
    )


class Lesson(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="описание урока",
        help_text="Добавьте описание",
    )
    preview = models.ImageField(
        blank=True, null=True, help_text="Добавьте заставку для урока"
    )
    url = models.URLField(
        blank=True,
        null=True,
        verbose_name="ссылка на урок",
        help_text="укажите ссылку на урок",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Название курса",
        help_text="Выберите, к какому курсу относится урок",
    )

    owner = models.ForeignKey(
        "users.User",
        on_delete=CASCADE,
        null=True,
        blank=True,
        verbose_name="Владелец",
        help_text="Владелец урока",
    )

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(
        "users.User",
        on_delete=CASCADE,
        verbose_name="Пользователь",
        help_text="Пользователь, оформивший подписку",
    )
    course = models.ForeignKey(
        Course,
        on_delete=CASCADE,
        verbose_name="Курс",
        help_text="Курс, на который оформлена подписка",
        related_name="subscriptions",
    )
