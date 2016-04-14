from django.core.management.base import BaseCommand
from notifications.email import email_notifications

class Command(BaseCommand):
    help = 'Email notifications'
    requires_system_checks = False
    def handle(self, **options):
        email_notifications()