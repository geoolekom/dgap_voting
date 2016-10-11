# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_bleach.models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_auto_20150924_1805'),
    ]

    operations = [
        migrations.CreateModel(
            name='QA',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('audience', models.CharField(choices=[('VOTING', 'Голосующему'), ('ORGANAZIER', 'Организатору голосования')], default='VOTING', max_length=30)),
                ('question', models.CharField(max_length=800)),
                ('answer', django_bleach.models.BleachField(max_length=800)),
            ],
            options={
                'verbose_name': 'Question/Answer',
                'verbose_name_plural': 'Faq',
            },
        ),
        migrations.AlterField(
            model_name='poll',
            name='target_group',
            field=models.CharField(verbose_name='Целевая группа', default='^', max_length=200),
        ),
        migrations.AlterField(
            model_name='poll',
            name='target_room',
            field=models.CharField(verbose_name='Целевая комната', default='^', max_length=200),
        ),
    ]
