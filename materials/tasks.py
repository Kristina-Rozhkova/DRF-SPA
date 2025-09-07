from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import ADMIN_EMAIL
from materials.models import Course, Subscription


@shared_task
def send_email(course_id=None):
    """Рассылка писем пользователям об обновлении материалов курса."""
    try:
        course = Course.objects.get(id=course_id)

        if timezone.now() - course.update_at >= timedelta(hours=4):
            subscriptions = Subscription.objects.filter(course=course)
            if subscriptions.exists():
                emails = [subscription.user.email for subscription in subscriptions]
                send_mail(
                    subject=f'Курс "{course.name}" обновлен',
                    message=f'Добрый день! Вы подписаны на обновление курса "{course.name}". Вы уже можете посмотреть '
                    f"их содержание с учетом изменений в личном кабинете.",
                    from_email=ADMIN_EMAIL,
                    recipient_list=emails,
                )
                print(f"Письма отправлены {len(emails)} подписчикам")
                return (
                    f"Уведомления отправлены для курса: {course.name} (ID: {course_id})"
                )

            return f"Нет подписчиков на курс: {course.name} (ID: {course_id})"

            course.notification_task_id = None
            course.save()
    except Exception as e:
        print(f"Ошибка: {str(e)}")
        send_email.retry(
            args=[course_id], kwargs={"delay_hours": 1}, exc=e, countdown=3600
        )
