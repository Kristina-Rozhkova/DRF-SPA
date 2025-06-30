from django.core.management import BaseCommand

from materials.models import Course
from users.models import Pay, User


class Command(BaseCommand):
    help = "Adding payment to the database"

    def handle(self, *args, **kwargs):
        user1, _ = User.objects.get_or_create(email="IvanovIvan@mail.ru")
        user2, _ = User.objects.get_or_create(email="Irina@gmail.com")
        user3, _ = User.objects.get_or_create(email="StanuslavStanislav@gmail.com")

        course1, _ = Course.objects.get_or_create(id=1)
        course2, _ = Course.objects.get_or_create(id=2)

        pays = [
            {
                "user": user1,
                "payment_date": "2024-07-28",
                "course": course1,
                "lesson": None,
                "amount": 150000,
                "form_of_payment": Pay.TRANSFER,
            },
            {
                "user": user2,
                "payment_date": "2023-04-28",
                "course": course1,
                "lesson": None,
                "amount": 150000,
                "form_of_payment": Pay.TRANSFER,
            },
            {
                "user": user3,
                "payment_date": "2021-12-28",
                "course": course2,
                "lesson": None,
                "amount": 130000,
                "form_of_payment": Pay.CASH,
            },
        ]

        for pay in pays:
            payment, created = Pay.objects.get_or_create(**pay)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Информация по оплате добавлена: {payment.user.email} - {payment.course.name}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Информация уже была добавлена ранее: {payment.user.email} - {payment.course.name}"
                    )
                )
