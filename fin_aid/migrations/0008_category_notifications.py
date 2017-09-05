# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fin_aid', '0007_auto_20170821_0320'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='notifications',
            field=models.BooleanField(verbose_name='Уведомления о новых заявлениях', default=True),
        ),
    ]
