# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import fin_aid.models


class Migration(migrations.Migration):

    dependencies = [
        ('fin_aid', '0004_monthlydata'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='monthlydata',
            options={'verbose_name': 'Информация о месяце', 'verbose_name_plural': 'Лимиты по месяцам'},
        ),
        migrations.AlterField(
            model_name='monthlydata',
            name='deadline_dttm',
            field=models.DateTimeField(verbose_name='Дэдлайн по заявлениям', default=fin_aid.models._get_default_deadline_dt),
        ),
        migrations.AlterField(
            model_name='monthlydata',
            name='month',
            field=models.IntegerField(verbose_name='Месяц', choices=[(1, 'Январь'), (2, 'Февраль'), (3, 'Март'), (4, 'Апрель'), (5, 'Май'), (6, 'Июнь'), (7, 'Июль'), (8, 'Август'), (9, 'Сентябрь'), (10, 'Октябрь'), (11, 'Ноябрь'), (12, 'Декабрь')], default=fin_aid.models._get_default_month),
        ),
        migrations.AlterField(
            model_name='monthlydata',
            name='payment_dttm',
            field=models.DateTimeField(verbose_name='Дата выплаты матпомощи', default=fin_aid.models._get_default_payment_dt),
        ),
        migrations.AlterField(
            model_name='monthlydata',
            name='year',
            field=models.IntegerField(verbose_name='Год', default=fin_aid.models._get_default_year),
        ),
    ]
