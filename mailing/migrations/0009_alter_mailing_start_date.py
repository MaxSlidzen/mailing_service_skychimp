# Generated by Django 4.2.5 on 2023-09-11 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0008_alter_mailing_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='start_date',
            field=models.DateField(verbose_name='дата старта рассылки'),
        ),
    ]
