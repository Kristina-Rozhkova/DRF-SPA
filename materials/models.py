from django.db import models


class Course(models.Model):
    name = models.CharField(
        max_length=50, verbose_name="Название", help_text="Введите название курса"
    )
    preview = models.ImageField(
        upload_to="materials/previews/courses",
        verbose_name="Картинка",
        help_text="Загрузите картинку",
        null=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Напишите описание курса",
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Создатель курса",
    )
    update_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата обновления курса"
    )
    notification_task_id = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="id задачи уведомления"
    )

    def __str__(self):
        return f"Курс: {self.name}\nОписание: {self.description}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(
        max_length=50, verbose_name="Название", help_text="Введите название урока"
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Напишите описание урока",
        null=True,
        blank=True,
    )
    preview = models.ImageField(
        upload_to="materials/previews/lessons",
        verbose_name="Картинка",
        help_text="Загрузите картинку",
        null=True,
        blank=True,
    )
    video = models.CharField(
        max_length=250,
        verbose_name="Ссылка на видео",
        help_text="Вставьте ссылку на видео",
        null=True,
        blank=True,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Курс",
        help_text="Укажите курс",
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Создатель урока",
    )
    update_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата обновления урока"
    )

    def __str__(self):
        return f"Курс: {self.course}" f"Урок: {self.name}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, verbose_name="Пользователь подписки"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Подписка на курс"
    )

    def __str__(self):
        return f"{self.user.email} подписан(а) на {self.course.name}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
