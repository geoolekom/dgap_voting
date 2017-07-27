# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cycle_storage', '0002_auto_20170727_2319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bicycle',
            name='manufacturer',
            field=models.CharField(blank=True, null=True, max_length=255, verbose_name='Производитель', default='Неизвестно'),
        ),
        migrations.AlterField(
            model_name='bicycle',
            name='model',
            field=models.CharField(blank=True, null=True, max_length=255, verbose_name='Модель', default='Неизвестно'),
        ),
        migrations.AlterField(
            model_name='place',
            name='bicycle',
            field=models.OneToOneField(null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, to='cycle_storage.Bicycle', default=None),
        ),
    ]
