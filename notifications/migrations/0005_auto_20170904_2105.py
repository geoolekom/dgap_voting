# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-04 18:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_auto_20170822_2222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usernotificationssettings',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]