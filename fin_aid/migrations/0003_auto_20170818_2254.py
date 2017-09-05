# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fin_aid', '0002_auto_20170802_1550'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='aiddocument',
            options={'verbose_name_plural': 'подтверждающие документы', 'verbose_name': 'потверждающий документ'},
        ),
        migrations.AlterModelOptions(
            name='aidrequest',
            options={'verbose_name_plural': 'заявления на матпомощь', 'verbose_name': 'заявление на матпомощь'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'категории', 'verbose_name': 'категория'},
        ),
    ]
