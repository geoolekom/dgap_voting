# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-13 21:00
from __future__ import unicode_literals

from django.db import migrations, models
import fin_aid.models


class Migration(migrations.Migration):

    dependencies = [
        ('fin_aid', '0013_auto_20171013_2012'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthlydata',
            name='student_dealine_dt',
            field=models.DateTimeField(default=fin_aid.models._get_default_deadline_dt, verbose_name='Дэдлайн по заявлениям'),
        ),
        migrations.AlterField(
            model_name='monthlydata',
            name='deadline_dt',
            field=models.DateField(default=fin_aid.models._get_default_deadline_dt, verbose_name='Дэдлайн по приказу'),
        ),
    ]
