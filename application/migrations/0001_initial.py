# Generated by Django 2.1.1 on 2018-09-02 20:34

import datetime
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Allowed_User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.TextField()),
                ('first_name', models.TextField()),
                ('last_name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Volunteer_Date',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.TextField()),
                ('event_begin', models.DateTimeField()),
                ('event_end', models.DateTimeField()),
                ('slots_total', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Volunteer_Date_Registration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marked', models.BooleanField(default=False)),
                ('attended', models.BooleanField(default=False)),
                ('signup_time', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('cancelled', models.BooleanField(default=False)),
                ('cancel_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='WIS_User',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_volunteer', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='volunteer_date_registration',
            name='volunteer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='registrations', to='application.WIS_User'),
        ),
        migrations.AddField(
            model_name='volunteer_date_registration',
            name='volunteer_date',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='registrations', to='application.Volunteer_Date'),
        ),
    ]
