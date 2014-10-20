# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20141017_2332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='cardnumber',
            field=models.CharField(verbose_name='Последние пять цифр номера социальной карты', null=True, blank=True, max_length=5),
        ),
    ]
