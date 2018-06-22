from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        if not User.objects.filter(email=settings.SUPERUSER_EMAIL).exists():
            User.objects.create_superuser(
                email=settings.SUPERUSER_EMAIL,
                password=settings.SUPERUSER_PASSWORD,
            )
