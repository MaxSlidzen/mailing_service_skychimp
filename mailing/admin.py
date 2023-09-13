from django.contrib import admin

from mailing.models import Client, Mailing, MailingLog


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'comment', 'added_by')
    list_filter = ('email', 'added_by',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('author', 'subject', 'status',)
    list_filter = ('subject', 'author',)


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('trying_datetime', 'status', 'mailing', 'client', 'error_message',)
    list_filter = ('mailing', 'client',)
