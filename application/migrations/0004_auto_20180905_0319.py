# Generated by Django 2.1.1 on 2018-09-05 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0003_wis_user_max_registrations'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Allowed_User',
        ),
        migrations.AddField(
            model_name='wis_user',
            name='nonce',
            field=models.TextField(blank=True, null=True),
        ),
    ]
