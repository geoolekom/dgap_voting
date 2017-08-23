# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fin_aid', '0008_category_notifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='aiddocument',
            name='is_application_paper',
            field=models.BooleanField(verbose_name='Заявление на матпомощь', default=False),
        ),
    ]
