# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20170727_0526'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bicycle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('manufacturer', models.CharField(null=True, blank=True, default='Unknown', max_length=255)),
                ('model', models.CharField(null=True, blank=True, default='Unknown', max_length=255)),
                ('add_dttm', models.DateTimeField(verbose_name='Publish datetime', auto_now_add=True)),
                ('photo', models.ImageField(upload_to='bicycles/')),
                ('verified', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(null=True, blank=True, to='profiles.UserProfile')),
            ],
            options={
                'verbose_name_plural': 'Велосипеды',
                'verbose_name': 'Велосипед',
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('bicycle', models.OneToOneField(null=True, default=None, blank=True, to='cycle_storage.Bicycle')),
            ],
            options={
                'verbose_name_plural': 'Места',
                'verbose_name': 'Место',
            },
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('dorm', models.CharField(null=True, blank=True, default='6', max_length=255)),
                ('name', models.CharField(max_length=255, default='Велокомната 6ки')),
            ],
            options={
                'verbose_name_plural': 'Велохранилища',
                'verbose_name': 'Велохранилище',
            },
        ),
        migrations.AddField(
            model_name='place',
            name='storage',
            field=models.ForeignKey(to='cycle_storage.Storage'),
        ),
    ]
