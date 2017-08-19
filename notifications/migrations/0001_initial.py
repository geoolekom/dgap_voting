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
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('send_dttm', models.DateTimeField(auto_now_add=True, verbose_name='Отправлено')),
                ('method', models.IntegerField(choices=[(1, 'e-mail'), (2, 'Вконтакте'), (3, 'telegram')], verbose_name='Способ')),
                ('text', models.TextField(max_length=1024, verbose_name='Текст')),
                ('result', models.CharField(max_length=256, verbose_name='Результат')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserNotificationsSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('allow_email', models.BooleanField(verbose_name='Разрешить уведомления на эл. почту', default=False)),
                ('allow_vk', models.BooleanField(verbose_name='Разрешить уведомления Вконтакте', default=True)),
                ('allow_telegram', models.BooleanField(verbose_name='Разрешить уведомления в Telegram', default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
