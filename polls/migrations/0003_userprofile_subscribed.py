# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_poll_times_mailed'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='subscribed',
            field=models.BooleanField(default=True, verbose_name='Пользователь подписан на рассылку'),
            preserve_default=True,
        ),
    ]
