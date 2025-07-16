from django.contrib import admin

from materials.models import Course, Lesson


@admin.register(Course)
class UserAdmin(admin.ModelAdmin):
    class Meta:
        list_filter = ("name", "owner")


@admin.register(Lesson)
class UserAdmin(admin.ModelAdmin):
    class Meta:
        list_filter = ("name", "owner", "course")
