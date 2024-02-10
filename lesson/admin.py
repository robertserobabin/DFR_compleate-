from django.contrib import admin

from lesson.models import Lesson, Course, Payments


@admin.register(Lesson)
class Admin(admin.ModelAdmin):
    list_display = ('title', 'description',)


@admin.register(Course)
class Admin(admin.ModelAdmin):
    list_display = ('title', 'description',)


@admin.register(Payments)
class Admin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'payment_method',)
