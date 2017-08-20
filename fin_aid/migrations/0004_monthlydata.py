# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import fin_aid.models
from datetime import datetime

class Migration(migrations.Migration):

    dependencies = [
        ('fin_aid', '0003_auto_20170818_2254'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthlyData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('year', models.IntegerField(verbose_name='Год', default=lambda: datetime.now().year)),
                ('month', models.IntegerField(verbose_name='Месяц', choices=[(1, 'Январь'), (2, 'Февраль'), (3, 'Март'), (4, 'Апрель'), (5, 'Май'), (6, 'Июнь'), (7, 'Июль'), (8, 'Август'), (9, 'Сентябрь'), (10, 'Октябрь'), (11, 'Ноябрь'), (12, 'Декабрь')])),
                ('limit', models.FloatField(verbose_name='Лимит')),
                ('deadline_dttm', models.DateTimeField(verbose_name='Дэдлайн по заявлениям')),
                ('payment_dttm', models.DateTimeField(verbose_name='Дата выплаты матпомощи')),
            ],
        ),
    ]
