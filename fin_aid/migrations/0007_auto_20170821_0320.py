# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fin_aid', '0006_auto_20170821_0313'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aidrequest',
            name='payment_dttm',
        ),
        migrations.AddField(
            model_name='aidrequest',
            name='payment_dt',
            field=models.DateField(null=True, verbose_name='Дата выплаты', blank=True),
        ),
    ]
