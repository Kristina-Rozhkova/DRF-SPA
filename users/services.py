import stripe
from forex_python.converter import CurrencyRates

from config.settings import STRIPE_API_KEY

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
