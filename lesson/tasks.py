import datetime
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from celery import shared_task
from lesson.models import Course
from users.models import User


@shared_task
def check_update():
    recipient_email = 'www.rufat@bk.ru'
    for i in Course.objects.all():
        if i.date_update > i.date_preview:
            send_mail(
                subject='Информация о курсе',
                message=f'Курс был обновлен',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[recipient_email]

            )
            i.date_preview = i.date_update
            i.save()


@shared_task
def check_update():
    a = timezone.now()
    for i in User.objects.all():
        count_date = a - i.last_login.replace(tzinfo=timezone.utc)
        if count_date > datetime.timedelta(days=30):
            i.role = 'member'
            i.save()


