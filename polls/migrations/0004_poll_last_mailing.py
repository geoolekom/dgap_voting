# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_userprofile_subscribed'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='last_mailing',
            field=models.DateTimeField(verbose_name='Последняя рассылка', null=True),
            preserve_default=True,
        ),
    ]
