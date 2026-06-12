import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create admin user from environment variables'

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get('ADMIN_USERNAME', '')
        password = os.environ.get('ADMIN_PASSWORD', '')
        email = os.environ.get('ADMIN_EMAIL', '')
        if not password:
            self.stdout.write('ADMIN_PASSWORD not set, skipping.')
            return
        if User.objects.filter(username=username).exists():
            self.stdout.write(f'User "{username}" already exists, skipping.')
            return
        User.objects.create_superuser(username=username, password=password, email=email)
        self.stdout.write(f'Superuser "{username}" created.')
