# Generated by Django 3.0.7 on 2020-06-21 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profile_is_online'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='is_online',
        ),
    ]
