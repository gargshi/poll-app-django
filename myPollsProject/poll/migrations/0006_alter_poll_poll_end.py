# Generated by Django 5.0.4 on 2024-05-26 14:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0005_alter_poll_poll_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='poll_end',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 26, 20, 32, 29, 977136), verbose_name='poll end'),
        ),
    ]