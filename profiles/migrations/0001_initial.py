# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LegacyDorm',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('dorm', models.IntegerField()),
                ('room', models.CharField(max_length=10)),
                ('group', models.CharField(max_length=10)),
                ('first_name', models.CharField(max_length=128)),
                ('middle_name', models.CharField(max_length=128)),
                ('last_name', models.CharField(max_length=128)),
                ('department', models.CharField(max_length=32)),
            ],
            options={
                'in_db': 'legacy_users',
                'managed': False,
                'db_table': 'dorm',
            },
        ),
        migrations.CreateModel(
            name='LegacyUser',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('group', models.CharField(max_length=100)),
                ('dorm', models.IntegerField()),
                ('room', models.CharField(max_length=10)),
                ('card', models.CharField(unique=True, max_length=64)),
                ('access_bicycle', models.IntegerField()),
                ('birthday', models.DateField(blank=True, null=True)),
                ('cardnumber', models.CharField(max_length=128)),
                ('date', models.DateTimeField()),
                ('expire', models.DateField(blank=True, null=True)),
                ('enabled', models.IntegerField()),
                ('access_laundry', models.IntegerField()),
                ('address_confirmed', models.IntegerField()),
                ('email', models.CharField(max_length=128)),
                ('phone', models.CharField(max_length=14)),
            ],
            options={
                'in_db': 'legacy_users',
                'managed': False,
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('dorm', models.IntegerField(default=0)),
                ('middlename', models.CharField(verbose_name='Отчество', blank=True, max_length=100)),
                ('group', models.CharField(verbose_name='Номер группы', blank=True, max_length=5)),
                ('room', models.CharField(verbose_name='Номер комнаты', blank=True, max_length=4)),
                ('is_approved', models.BooleanField(verbose_name='Пользователь подтверждён', default=False)),
                ('is_subscribed', models.BooleanField(verbose_name='Пользователь подписан на рассылку', default=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
