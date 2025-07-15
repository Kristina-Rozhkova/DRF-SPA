import stripe
from forex_python.converter import CurrencyRates
import json
from datetime import datetime, timedelta
from config.settings import STRIPE_API_KEY
from django_celery_beat.models import PeriodicTask, IntervalSchedule

stripe.api_key = STRIPE_API_KEY


def converter(amount):
    """Конвертирование валюты: рубли в доллары."""

    c = CurrencyRates()
    rate = c.get_rate("RUB", "USD")
    return int(amount * rate)


def create_stripe_price(amount):
    """Создание цены в stripe."""

    return stripe.Price.create(
        currency="usd",
        unit_amount=amount * 100,
        product_data={"name": "Pay for material"},
    )


def create_stripe_sessions(price):
    """Создание сессии на оплату в stripe."""

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/materials/",
        line_items=[{"price": price.id, "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")


def check_payment_status(session_id):
    """Проверка статуса оплаты по ID сессии."""

    session = stripe.checkout.Session.retrieve(session_id)
    return {
        "status": session.status,
        "payment_status": session.payment_status,
        "user_email": session.customer_details.email,
    }

# def set_schedule(*args, **kwargs):
#     """ Установка расписания для задачи по блокировке пользователей. """
#     schedule, created = IntervalSchedule.objects.get_or_create(
#         every=10,
#         period=IntervalSchedule.SECONDS,
#     )
#
#     PeriodicTask.objects.create(
#         interval=schedule,  # we created this above.
#         name='Importing contacts',  # simply describes this periodic task.
#         task='users.tasks.deactivate_inactive_users',  # name of task.
#         args=json.dumps(['arg1', 'arg2']),
#         kwargs=json.dumps({
#             'be_careful': True,
#         }),
#         expires=datetime.utcnow() + timedelta(seconds=30)
#     )
