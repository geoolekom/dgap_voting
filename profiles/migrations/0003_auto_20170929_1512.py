# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-29 12:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_studentinfo_sex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentinfo',
            name='course',
            field=models.IntegerField(default=0, verbose_name='Курс'),
        ),
    ]