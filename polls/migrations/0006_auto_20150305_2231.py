# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20150304_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='times_mailed',
            field=models.IntegerField(blank=True, default=0),
            preserve_default=True,
        ),
    ]
