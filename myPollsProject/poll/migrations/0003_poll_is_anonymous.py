# Generated by Django 5.0.4 on 2024-05-24 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0002_poll_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='is_anonymous',
            field=models.BooleanField(default=False),
        ),
    ]
