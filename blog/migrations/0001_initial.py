# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20170822_2233'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('slug', models.SlugField(verbose_name='URL')),
                ('title', models.CharField(blank=True, null=True, default=None, max_length=255, verbose_name='Заголовок')),
                ('publish_dttm', models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True)),
                ('content', models.TextField(verbose_name='Контент', max_length=10000)),
                ('hidden', models.BooleanField(verbose_name='Скрытый', default=False)),
                ('show_in_feed', models.BooleanField(verbose_name='ПОказывать в ленте', default=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.UserProfile')),
            ],
            options={
                'verbose_name': 'пост',
                'verbose_name_plural': 'посты',
            },
        ),
    ]
