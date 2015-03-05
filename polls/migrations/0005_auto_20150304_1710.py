# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_poll_last_mailing'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='subscribed',
            new_name='is_subscribed',
        ),
    ]
