# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20141017_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='choices_order',
            field=models.CharField(default='created', verbose_name='Порядок вариантов ответа', max_length=10, choices=[('created', 'В порядке создания'), ('?', 'В случайном порядке')]),
        ),
    ]
