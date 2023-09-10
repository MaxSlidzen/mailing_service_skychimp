from mailing.models import Mailing, Client


def count_all_mailings():
    return len(Mailing.objects.all())


def count_active_mailings():
    return len(Mailing.objects.filter(status='started'))


def count_unique_clients():
    clients = set()
    for client in Client.objects.all():
        clients.add(client.email)
    return len(clients)
