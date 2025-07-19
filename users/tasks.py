from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from .models import User


@shared_task
def deactivate_inactive_users():
    """Блокировка пользователей, которые не заходили более месяца"""
    month_ago = timezone.now() - timedelta(days=30)
    count = 0

    filter_login = {"last_login__lte": month_ago, "is_active": True}
    inactive_users = User.objects.filter(**filter_login)

    if inactive_users.exists():
        for user in inactive_users:
            user.update(is_active=False)
            count += 1

    return f"Заблокировано {count} неактивных пользователей"
