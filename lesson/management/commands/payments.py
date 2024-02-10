from django.core.management import BaseCommand
from lesson.models import Payments
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user_email = '1@mail.ru'
        user = User.objects.get(email=user_email)
        payments = Payments.objects.create(
            user=user,
            data_payments='2023-01-19',
            paid_course='lesson',
            payment_method='transfer'

        )
        payments.save()