# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_auto_20170819_1657'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'verbose_name': 'Уведомление', 'verbose_name_plural': 'Уведомления'},
        ),
        migrations.AlterModelOptions(
            name='usernotificationssettings',
            options={'verbose_name': 'настройки уведомлений пользователя', 'verbose_name_plural': 'настройки уведомлений пользователей'},
        ),
    ]
