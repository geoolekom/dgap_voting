# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cycle_storage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bicycle',
            name='manufacturer',
            field=models.CharField(blank=True, max_length=255, verbose_name='Производитель', null=True, default='Unknown'),
        ),
        migrations.AlterField(
            model_name='bicycle',
            name='model',
            field=models.CharField(blank=True, max_length=255, verbose_name='Модель', null=True, default='Unknown'),
        ),
        migrations.AlterField(
            model_name='bicycle',
            name='photo',
            field=models.ImageField(upload_to='bicycles/', verbose_name='Фотография'),
        ),
        migrations.AlterField(
            model_name='storage',
            name='dorm',
            field=models.CharField(blank=True, max_length=255, verbose_name='Общежитие', null=True, default='6'),
        ),
        migrations.AlterField(
            model_name='storage',
            name='name',
            field=models.CharField(max_length=255, default='Велокомната 6ки', verbose_name='Номер места'),
        ),
    ]
