# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20170727_0526'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=255, blank=True, default=None, null=True)),
                ('publish_dttm', models.DateTimeField(verbose_name='Publish datetime', auto_now_add=True)),
                ('content', models.TextField(max_length=10000)),
                ('author', models.ForeignKey(to='profiles.UserProfile', null=True, blank=True)),
            ],
        ),
    ]
