from django.core.management.base import BaseCommand
from mailing.services import send_mailing

class Command(BaseCommand):
    help = "Send scheduled mailings"

    def handle(self, *args, **kwargs):
        send_mailing()
        self.stdout.write("Mailing process completed")