# Generated by Django 3.2.10 on 2021-12-12 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MLSite', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resume',
            old_name='vacancy_user_id',
            new_name='vacancy_user',
        ),
        migrations.RenameField(
            model_name='vacancy',
            old_name='vacancy_user_id',
            new_name='vacancy_user',
        ),
    ]
