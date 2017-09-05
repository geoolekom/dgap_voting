# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LegacyDorm',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('dorm', models.IntegerField()),
                ('room', models.CharField(max_length=10)),
                ('group', models.CharField(max_length=10)),
                ('first_name', models.CharField(max_length=128)),
                ('middle_name', models.CharField(max_length=128)),
                ('last_name', models.CharField(max_length=128)),
                ('department', models.CharField(max_length=32)),
            ],
            options={
                'managed': False,
                'db_table': 'dorm',
                'in_db': 'legacy_users',
            },
        ),
        migrations.CreateModel(
            name='LegacyUser',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('group', models.CharField(max_length=100)),
                ('dorm', models.IntegerField()),
                ('room', models.CharField(max_length=10)),
                ('card', models.CharField(unique=True, max_length=64)),
                ('access_bicycle', models.IntegerField()),
                ('birthday', models.DateField(null=True, blank=True)),
                ('cardnumber', models.CharField(max_length=128)),
                ('date', models.DateTimeField()),
                ('expire', models.DateField(null=True, blank=True)),
                ('enabled', models.IntegerField()),
                ('access_laundry', models.IntegerField()),
                ('address_confirmed', models.IntegerField()),
                ('email', models.CharField(max_length=128)),
                ('phone', models.CharField(max_length=14)),
            ],
            options={
                'managed': False,
                'db_table': 'users',
                'in_db': 'legacy_users',
            },
        ),
        migrations.CreateModel(
            name='StudentInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('fio', models.CharField(verbose_name='ФИО', null=True, max_length=100, blank=True)),
                ('group', models.CharField(verbose_name='Группа', null=True, max_length=10, blank=True)),
                ('course', models.IntegerField(default=0)),
                ('phystech', models.CharField(verbose_name='phystech.edu', null=True, max_length=50, blank=True)),
                ('vk', models.CharField(verbose_name='vk', null=True, max_length=50, blank=True)),
                ('first_name', models.CharField(verbose_name='Имя', null=True, max_length=100, blank=True)),
                ('last_name', models.CharField(verbose_name='Фамилия', null=True, max_length=100, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('dorm', models.IntegerField(default=0)),
                ('middlename', models.CharField(verbose_name='Отчество', max_length=100, blank=True)),
                ('group', models.CharField(verbose_name='Номер группы', max_length=10, blank=True)),
                ('room', models.CharField(verbose_name='Номер комнаты', max_length=4, blank=True)),
                ('is_approved', models.BooleanField(verbose_name='Пользователь подтверждён', default=False)),
                ('is_subscribed', models.BooleanField(verbose_name='Пользователь подписан на рассылку', default=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
                ('student_info', models.ForeignKey(to='profiles.StudentInfo', null=True, default=None, blank=True)),
            ],
        ),
    ]
