# Generated by Django 3.2.10 on 2021-12-18 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MLSite', '0009_auto_20211218_2232'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vacancy',
            name='highlighted',
        ),
    ]
