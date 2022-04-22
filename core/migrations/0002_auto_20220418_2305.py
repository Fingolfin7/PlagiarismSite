# Generated by Django 3.2.9 on 2022-04-18 21:05

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserHistory',
            new_name='History',
        ),
        migrations.RenameModel(
            old_name='Uploads',
            new_name='Upload',
        ),
        migrations.AlterModelOptions(
            name='history',
            options={'verbose_name_plural': 'History'},
        ),
    ]
