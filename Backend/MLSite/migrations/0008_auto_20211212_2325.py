# Generated by Django 3.2.10 on 2021-12-12 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MLSite', '0007_auto_20211212_2143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
    ]