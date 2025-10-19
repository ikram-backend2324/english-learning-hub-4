# accounts/management/commands/create_default_superuser.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class Command(BaseCommand):
    help = "Create superuser with username/password only"

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not password:
            self.stdout.write(
                self.style.ERROR("❌ DJANGO_SUPERUSER_PASSWORD not set")
            )
            return

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                password=password,
                name="Admin",
                role="admin"
            )
            self.stdout.write(
                self.style.SUCCESS(f"✅ Superuser '{username}' created")
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"⚠️ User '{username}' already exists")
            )