# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-29 13:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20170929_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentinfo',
            name='room',
            field=models.CharField(blank=True, max_length=32, verbose_name='Номер комнаты'),
        ),
    ]
