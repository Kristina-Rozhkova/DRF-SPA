# Generated by Django 5.2.3 on 2025-07-06 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("materials", "0005_course_update_at_lesson_update_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="notification_task_id",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
