# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20141017_2317'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='choice',
            options={},
        ),
        migrations.AlterOrderWithRespectTo(
            name='choice',
            order_with_respect_to='poll',
        ),
    ]
