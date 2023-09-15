from django import template

from mailing.models import Mailing, Client

register = template.Library()


@register.filter
def full_name(person):
    """
    Полное представление ФИО клиента/пользователя
    """
    try:
        return (f'{"" if person.first_name is None else person.first_name} '
                f'{"" if person.last_name is None else person.last_name} '
                f'{"" if person.patronic_name is None else person.patronic_name}')

    # Ошибка возникает при составлении полного имени пользователя, поскольку отсутствует поле "Отчество"
    except AttributeError:
        return (f'{"" if person.first_name is None else person.first_name} '
                f'{"" if person.last_name is None else person.last_name}')


@register.simple_tag
def all_mailings():
    """
    Количества всех рассылок
    """
    return len(Mailing.objects.all())


@register.simple_tag
def active_mailings():
    """
    Количества активных (незавершенных) рассылок
    """
    return len(Mailing.objects.filter(status='started'))


@register.simple_tag
def unique_clients():
    """
    Количество уникальных клиентов сервиса (по электронной почте)
    """
    clients = set()
    for client in Client.objects.all():
        clients.add(client.email)
    return len(clients)
