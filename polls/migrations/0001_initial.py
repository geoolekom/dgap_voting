# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('choice_text', models.CharField(verbose_name='Текст ответа', max_length=800)),
                ('votes', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='Название опроса', max_length=200)),
                ('question', models.CharField(verbose_name='Вопрос', max_length=200)),
                ('begin_date', models.DateTimeField(verbose_name='Начало голосования')),
                ('end_date', models.DateTimeField(verbose_name='Конец голосования')),
                ('target_room', models.CharField(verbose_name='Целевая комната', max_length=200, default='^\\d\\d\\d.?.?$')),
                ('target_group', models.CharField(verbose_name='Целевая группа', max_length=200, default='^\\d\\d\\d\\d?.?$')),
                ('public', models.BooleanField(verbose_name='Открытое голосование', default=True)),
                ('answer_type', models.CharField(verbose_name='Тип ответа', max_length=10, default='ONE', choices=[('ONE', 'Выбор одного варианта'), ('MANY', 'Выбор нескольких вариантов'), ('OWN', 'Свой вариант')])),
                ('voted_users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserHash',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('value', models.BigIntegerField()),
                ('choice', models.ForeignKey(to='polls.Choice')),
                ('user', models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL, default=None)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('dorm', models.IntegerField(default=0)),
                ('middlename', models.CharField(verbose_name='Отчество', max_length=100, blank=True)),
                ('group', models.CharField(verbose_name='Номер группы', max_length=5, blank=True)),
                ('room', models.CharField(verbose_name='Номер комнаты', max_length=4, blank=True)),
                ('approval', models.BooleanField(verbose_name='Пользователь подтверждён', default=False)),
                ('cardnumber', models.IntegerField(verbose_name='Последние пять цифр номера социальной карты', max_length=5, null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='choice',
            name='poll',
            field=models.ForeignKey(to='polls.Poll'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='LegacyDorm',
            fields=[
            ],
            options={
                'in_db': 'legacy_users',
                'db_table': 'dorm',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LegacyUser',
            fields=[
            ],
            options={
                'in_db': 'legacy_users',
                'db_table': 'users',
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
