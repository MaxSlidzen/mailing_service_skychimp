import datetime
import smtplib
import socket
from calendar import monthrange, IllegalMonthError

from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.utils import timezone

from mailing.models import Mailing, MailingLog, Client


def send_mailing():
    mailings = Mailing.objects.exclude(status='done')
    current_datetime = timezone.now()

    for mailing in mailings:
        if mailing.stop_date is None or mailing.stop_date > current_datetime.date():

            if mailing.start_date <= current_datetime.date() and mailing.time <= datetime.datetime.now().time():

                if mailing.status == 'created':
                    mailing.status = 'started'
                    mailing.save()

                clients = mailing.client.all()
                last_log = MailingLog.objects.filter(mailing=mailing).last()

                if last_log is None or last_log.status == 'failed' or (

                        mailing.period == 'daily' and (
                        current_datetime.date() - last_log.trying_datetime.date()) >= datetime.timedelta(days=1)) or (

                        mailing.period == 'weekly' and (
                        current_datetime.date() - last_log.trying_datetime.date()) >= datetime.timedelta(days=7)) or (

                        mailing.period == 'monthly' and (
                        current_datetime.date() - last_log.trying_datetime.date()) >= datetime.timedelta(days=count_days())):

                    send_to_clients(clients, mailing)
        else:
            mailing.status = 'done'
            mailing.save()


def send_to_clients(persons, letter):
    for person in persons:
        try:
            send_mail(
                subject=letter.subject,
                message=letter.message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[person.email],
                fail_silently=False,
            )
            log = MailingLog(status='ok', client=person, mailing=letter, error_message='Отправка прошла успешно')
            log.save()
        except smtplib.SMTPAuthenticationError as e:
            log = MailingLog(status='failed', client=person, mailing=letter,
                             error_message=f'{e}. Ошибка авторизации. Необходимо проверить настройки почты '
                                           f'(EMAIL_HOST_USER/EMAIL_HOST_PASSWORD)')
            log.save()
        except smtplib.SMTPException as e:
            log = MailingLog(status='failed', client=person, mailing=letter,
                             error_message=f'{e}. Ошибка.')
            log.save()
        except socket.gaierror as e:
            log = MailingLog(status='failed', client=person, mailing=letter,
                             error_message=f'{e}. Ошибка подключения. Необходимо проверить подключение к интернету '
                                           f'или настройки почты (EMAIL_HOST)')
            log.save()
        except OSError as e:
            log = MailingLog(status='failed', client=person, mailing=letter,
                             error_message=f'{e}. Ошибка. Необходимо проверить настройки почты (EMAIL_PORT)')
            log.save()


def count_days():
    last_month = datetime.date.today().month - 1
    current_year = datetime.date.today().year

    # Обработка ошибки, если текущий месяц - январь
    try:
        days = monthrange(current_year, last_month)[1]
    except IllegalMonthError:
        days = 31

    return days


def get_cache_mailing(mailing_item):
    if settings.CACHE_ENABLED:
        key_clients = f'clients_mailing_{mailing_item.pk}'
        key_logs = f'logs_mailing_{mailing_item.pk}'
        cache_data_clients = cache.get(key_clients)
        cache_data_logs = cache.get(key_logs)
        print(cache_data_clients)
        print(cache_data_logs)
        if cache_data_clients is None:
            cache_data_clients = Client.objects.filter(mailing=mailing_item)
            cache.set(key_clients, cache_data_clients)
        if cache_data_logs is None:
            cache_data_logs = MailingLog.objects.filter(mailing=mailing_item).order_by('-pk')[:len(cache_data_clients)]
            cache.set(key_logs, cache_data_logs)

        return cache_data_clients, cache_data_logs
    else:
        clients = Client.objects.filter(mailing=mailing_item)
        logs = MailingLog.objects.filter(mailing=mailing_item).order_by('-pk')[:len(clients)]
        return clients, logs
