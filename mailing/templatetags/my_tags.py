from django import template

register = template.Library()


@register.filter
def full_name(client):
    return f'{client.first_name} {client.last_name} {"" if client.patronic_name is None else client.patronic_name}'
