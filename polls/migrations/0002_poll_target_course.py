# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-29 12:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='target_course',
            field=models.CharField(default='^', max_length=200, verbose_name='Курсы, которые голосуют'),
        ),
    ]
