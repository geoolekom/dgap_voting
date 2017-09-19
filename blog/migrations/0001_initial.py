# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-08 11:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(verbose_name='URL')),
                ('title', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Заголовок')),
                ('publish_dttm', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('content', models.TextField(max_length=10000, verbose_name='Контент')),
                ('hidden', models.BooleanField(default=False, verbose_name='Скрытый')),
                ('show_in_feed', models.BooleanField(default=True, verbose_name='ПОказывать в ленте')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.UserProfile')),
            ],
            options={
                'verbose_name_plural': 'посты',
                'verbose_name': 'пост',
            },
        ),
    ]