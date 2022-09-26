from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.conf import settings
User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a superuser.'

    def handle(self, *args, **options):
        if not User.objects.filter(username='alex2').exists():
            User.objects.create_superuser(
                username='alex2',
                email='alex25@hootmail.com',
                password='complexpassword123'
            )
        print('Superuser has been created.')