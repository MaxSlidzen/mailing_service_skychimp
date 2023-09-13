from django.core.management import BaseCommand

from mailing.models import Mailing
from mailing.services import send_to_clients


class Command(BaseCommand):
    """
    Отправка сообщений по всем незавершенным рассылкам вне зависимости от расписания
    """
    def handle(self, *args, **kwargs):
        mailings = Mailing.objects.exclude(status='done')
        for mailing in mailings:
            clients = mailing.client.all()
            send_to_clients(clients, mailing)
