# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-08-09 14:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('departments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activist',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activists', to='departments.Department', verbose_name='отдел'),
        ),
        migrations.AlterField(
            model_name='department',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]