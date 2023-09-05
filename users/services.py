from django.core.mail import send_mail

from django.conf import settings

from users.models import User


def send_verify_email(user_item: User):
    send_mail(
        'Подтверждение регистрации',
        f'Пройдите по следующей ссылке для подтверждения регистрации '
        f'127.0.0.1:8000/users/verify_{user_item.verify_token}',
        settings.EMAIL_HOST_USER,
        [user_item.email]
    )
