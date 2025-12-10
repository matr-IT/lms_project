from django.db import models


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

    def __str__(self):
        return self.name