from datetime import date

from django.conf import settings
from django.db import models

from users.models import NULLABLE


class Client(models.Model):
    email = models.EmailField(verbose_name='email')
    first_name = models.CharField(max_length=100, verbose_name='имя')
    last_name = models.CharField(max_length=100, verbose_name='фамилия')
    patronic_name = models.CharField(max_length=100, **NULLABLE, verbose_name='отчество')
    comment = models.TextField(verbose_name='комментарий')

    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE,
                                 verbose_name='добавлен пользователем')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Mailing(models.Model):
    PERIOD_DAILY = 'daily'
    PERIOD_WEEKLY = 'weekly'
    PERIOD_MONTHLY = 'monthly'

    PERIODS = (
        (PERIOD_DAILY, 'Ежедневная'),
        (PERIOD_WEEKLY, 'Раз в неделю'),
        (PERIOD_MONTHLY, 'Раз в месяц'),
    )

    STATUS_CREATED = 'created'
    STATUS_STARTED = 'started'
    STATUS_DONE = 'done'
    STATUSES = (
        (STATUS_STARTED, 'Активна'),
        (STATUS_CREATED, 'Создана'),
        (STATUS_DONE, 'Неактивна'),
    )

    start_date = models.DateField(default=date.today(), verbose_name='дата старта рассылки')
    stop_date = models.DateField(**NULLABLE, verbose_name='дата завершения рассылки')
    time = models.TimeField(verbose_name='время отправки')
    period = models.CharField(max_length=20, choices=PERIODS, verbose_name='периодичность')
    status = models.CharField(max_length=20, default='created', choices=STATUSES, verbose_name='статус рассылки')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE,
                               verbose_name='автор рассылки')
    client = models.ManyToManyField(Client, verbose_name='клиент')

    subject = models.CharField(max_length=100, verbose_name='тема')
    message = models.TextField(verbose_name='сообщение')

    def __str__(self):
        return f'{self.subject} ({self.author})'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class MailingLog(models.Model):
    STATUS_OK = 'ok'
    STATUS_FAILED = 'failed'
    STATUSES = (
        (STATUS_OK, 'Успешно'),
        (STATUS_FAILED, 'Ошибка'),
    )

    trying_datetime = models.DateTimeField(auto_now_add=True, verbose_name='дата и время попытки')
    status = models.CharField(max_length=20, choices=STATUSES, verbose_name='статус попытки')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='клиент')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='рассылка')
    error_message = models.TextField(**NULLABLE, verbose_name='сообщение ошибки')

    def __str__(self):
        return f'{self.mailing}[{self.client}] - {self.status}'

    class Meta:
        verbose_name = 'лог рассылки'
        verbose_name_plural = 'логи рассылки'
