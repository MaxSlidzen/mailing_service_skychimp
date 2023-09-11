from django import template

from mailing.models import Mailing, Client

register = template.Library()


@register.filter
def full_name(person):
    try:
        return f'{person.first_name} {person.last_name} {"" if person.patronic_name is None else person.patronic_name}'
    except AttributeError:
        return f'{person.first_name} {person.last_name}'


@register.simple_tag
def all_mailings():
    return len(Mailing.objects.all())


@register.simple_tag
def active_mailings():
    return len(Mailing.objects.filter(status='started'))


@register.simple_tag
def unique_clients():
    clients = set()
    for client in Client.objects.all():
        clients.add(client.email)
    return len(clients)
