# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import fin_aid.models


class Migration(migrations.Migration):

    dependencies = [
        ('fin_aid', '0005_auto_20170821_0054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monthlydata',
            name='deadline_dttm',
        ),
        migrations.RemoveField(
            model_name='monthlydata',
            name='payment_dttm',
        ),
        migrations.AddField(
            model_name='monthlydata',
            name='deadline_dt',
            field=models.DateField(default=fin_aid.models._get_default_deadline_dt, verbose_name='Дэдлайн по заявлениям'),
        ),
        migrations.AddField(
            model_name='monthlydata',
            name='payment_dt',
            field=models.DateField(default=fin_aid.models._get_default_payment_dt, verbose_name='Дата выплаты матпомощи'),
        ),
    ]
