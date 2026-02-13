"""
Management command to create/update admin user with credentials.
Username: Little, Password: Littlesam@97
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Create or update admin user (Little / Littlesam@97)"

    def handle(self, *args, **options):
        username = "Little"
        password = "Littlesam@97"
        email = "little@sachrisclub.com"

        user, created = User.objects.update_or_create(
            username=username,
            defaults={
                'email': email,
                'is_superuser': True,
                'is_staff': True,
                'is_active': True,
            }
        )
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created admin user "{username}" with password {password}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Updated admin user "{username}" with new password'))
