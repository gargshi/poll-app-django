# Generated by Django 5.0.4 on 2024-05-28 07:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0007_alter_poll_poll_end_vote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='poll_end',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 28, 14, 25, 50, 807080), verbose_name='poll end'),
        ),
        migrations.AlterModelTable(
            name='vote',
            table='votes',
        ),
    ]
