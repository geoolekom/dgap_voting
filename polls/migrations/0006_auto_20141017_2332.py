# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20141017_2327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='choices_order',
            field=models.CharField(choices=[('created', 'В порядке добавления'), ('?', 'В случайном порядке')], max_length=10, default='created', verbose_name='Порядок вариантов ответа'),
        ),
        migrations.AlterOrderWithRespectTo(
            name='choice',
            order_with_respect_to=None,
        ),
    ]
