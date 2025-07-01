from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(
        verbose_name="Электронная почта",
        help_text="Укажите электронную почту",
        unique=True,
    )
    phone = models.CharField(
        verbose_name="Номер телефона",
        help_text="Укажите номер телефона",
        max_length=35,
        null=True,
        blank=True,
    )
    city = models.CharField(
        verbose_name="Город",
        help_text="Укажите город",
        max_length=50,
        null=True,
        blank=True,
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        null=True,
        blank=True,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Pay(models.Model):
    CASH = "Наличные"
    TRANSFER = "Перевод на счет"

    PAYMENT_IN_CHOICES = [(CASH, "Наличные"), (TRANSFER, "Перевод")]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="user",
        verbose_name="Пользователь",
        null=True,
        blank=True,
    )
    payment_date = models.DateField(auto_now_add=True, verbose_name="Дата оплаты")
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Оплаченный курс",
        null=True,
        blank=True,
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        verbose_name="Оплаченный урок",
        null=True,
        blank=True,
    )
    amount = models.PositiveIntegerField(
        verbose_name="Сумма оплаты", help_text="Введите сумму оплаты"
    )
    form_of_payment = models.CharField(
        max_length=15,
        choices=PAYMENT_IN_CHOICES,
        verbose_name="Способ оплаты",
        help_text="Выберите способ оплаты",
        null=True,
        blank=True,
    )
    session_id = models.CharField(
        verbose_name="Id сессии",
        help_text="Укажите id сессии",
        max_length=255,
        null=True,
        blank=True,
    )
    link = models.URLField(
        max_length=400,
        verbose_name="Ссылка на оплату",
        help_text="Укажите ссылку на оплату",
        null=True,
        blank=True,
    )
    payment_status = models.CharField(
        max_length=20,
        default="unpaid",
        verbose_name="Статус оплаты",
        help_text="Укажите статус оплаты",
        null=True,
        blank=True,
    )

    def __str__(self):
        if self.course:
            return (
                f"{self.user} оплатил курс {self.course} {self.payment_date} в размере {self.amount}. Способ оплаты"
                f" - {self.form_of_payment}."
            )
        return (
            f"{self.user} оплатил урок {self.lesson} {self.payment_date} в размере {self.amount}. Способ оплаты"
            f" - {self.form_of_payment}."
        )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
