from django.core.cache import cache
from django.core.mail import send_mail

from django.conf import settings

from mailing.models import Mailing
from users.models import User


def send_verify_email(user_item: User):
    send_mail(
        'Подтверждение регистрации',
        f'Пройдите по следующей ссылке для подтверждения регистрации '
        f'127.0.0.1:8000/users/verify_{user_item.verify_token}',
        settings.EMAIL_HOST_USER,
        [user_item.email]
    )


def get_cache_user(user_item):
    """
    Кеширование данных по рассылкам пользователя
    """
    if settings.CACHE_ENABLED:
        key = f'user_mailings_{user_item.pk}'
        cache_data_mailings = cache.get(key)
        if cache_data_mailings is None:
            cache_data_mailings = Mailing.objects.filter(author=user_item)
            cache.set(key, cache_data_mailings)

        return cache_data_mailings

    return Mailing.objects.filter(mailing=user_item)
