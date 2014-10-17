# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='created',
            field=models.DateTimeField(null=True, editable=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='poll',
            name='choices_order',
            field=models.CharField(default='created', max_length=10, choices=[('created', 'В порядке создания'), ('?', 'В случайном порядке')], verbose_name='Порядок вариантов ответа'),
            preserve_default=True,
        ),
    ]
