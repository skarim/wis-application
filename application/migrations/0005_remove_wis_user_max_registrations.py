# Generated by Django 2.1.1 on 2018-09-08 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0004_auto_20180905_0319'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wis_user',
            name='max_registrations',
        ),
    ]
