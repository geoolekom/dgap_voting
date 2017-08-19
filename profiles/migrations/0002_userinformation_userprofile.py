# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInformation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('fio', models.CharField(blank=True, verbose_name='ФИО', max_length=100, null=True)),
                ('group', models.CharField(blank=True, verbose_name='Группа', max_length=10, null=True)),
                ('course', models.IntegerField(default=0)),
                ('phystech', models.CharField(blank=True, verbose_name='phystech.edu', max_length=50, null=True)),
                ('vk', models.CharField(blank=True, verbose_name='vk', max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('dorm', models.IntegerField(default=0)),
                ('middlename', models.CharField(blank=True, verbose_name='Отчество', max_length=100)),
                ('group', models.CharField(blank=True, verbose_name='Номер группы', max_length=10)),
                ('room', models.CharField(blank=True, verbose_name='Номер комнаты', max_length=4)),
                ('is_approved', models.BooleanField(verbose_name='Пользователь подтверждён', default=False)),
                ('is_subscribed', models.BooleanField(verbose_name='Пользователь подписан на рассылку', default=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
                ('user_information', models.ForeignKey(default=None, to='profiles.UserInformation', null=True, blank=True)),
            ],
        ),
    ]
