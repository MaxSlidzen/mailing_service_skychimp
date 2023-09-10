from django import template

register = template.Library()


@register.filter
def full_name(person):
    try:
        return f'{person.first_name} {person.last_name} {"" if person.patronic_name is None else person.patronic_name}'
    except AttributeError:
        return f'{person.first_name} {person.last_name}'
