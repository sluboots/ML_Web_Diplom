# Generated by Django 3.2.10 on 2021-12-12 16:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MLSite', '0005_auto_20211212_2129'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resume',
            old_name='created_at',
            new_name='created_by',
        ),
        migrations.RenameField(
            model_name='vacancy',
            old_name='created_at',
            new_name='created_by',
        ),
    ]
