# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20141017_2221'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='choice',
            options={'ordering': ['poll__choices_order']},
        ),
        migrations.AlterField(
            model_name='poll',
            name='choices_order',
            field=models.CharField(max_length=10, default='-created', verbose_name='Порядок вариантов ответа', choices=[('-created', 'В порядке создания'), ('?', 'В случайном порядке')]),
        ),
    ]
