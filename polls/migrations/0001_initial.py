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
            name='LegacyDorm',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('dorm', models.IntegerField()),
                ('room', models.CharField(max_length=10)),
                ('group', models.CharField(max_length=10)),
                ('first_name', models.CharField(max_length=128)),
                ('middle_name', models.CharField(max_length=128)),
                ('last_name', models.CharField(max_length=128)),
                ('department', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'dorm',
                'in_db': 'legacy_users',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LegacyUser',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('group', models.CharField(max_length=100)),
                ('dorm', models.IntegerField()),
                ('room', models.CharField(max_length=10)),
                ('card', models.CharField(unique=True, max_length=64)),
                ('access_bicycle', models.IntegerField()),
                ('birthday', models.DateField(null=True, blank=True)),
                ('cardnumber', models.CharField(max_length=128)),
                ('date', models.DateTimeField()),
                ('expire', models.DateField(null=True, blank=True)),
                ('enabled', models.IntegerField()),
                ('access_laundry', models.IntegerField()),
                ('address_confirmed', models.IntegerField()),
                ('email', models.CharField(max_length=128)),
                ('phone', models.CharField(max_length=14)),
            ],
            options={
                'db_table': 'users',
                'in_db': 'legacy_users',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('choice_text', models.CharField(max_length=800, verbose_name='Текст ответа')),
                ('votes', models.IntegerField(default=0)),
                ('created', models.DateTimeField(null=True, editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=200, verbose_name='Название опроса')),
                ('question', models.CharField(max_length=200, verbose_name='Вопрос')),
                ('begin_date', models.DateTimeField(verbose_name='Начало голосования')),
                ('end_date', models.DateTimeField(verbose_name='Конец голосования')),
                ('target_room', models.CharField(max_length=200, verbose_name='Целевая комната', default='^\\d\\d\\d.?.?$')),
                ('target_group', models.CharField(max_length=200, verbose_name='Целевая группа', default='^\\d\\d\\d\\d?.?$')),
                ('public', models.BooleanField(verbose_name='Открытое голосование', default=True)),
                ('answer_type', models.CharField(choices=[('ONE', 'Выбор одного варианта'), ('MANY', 'Выбор нескольких вариантов'), ('OWN', 'Свой вариант')], max_length=10, verbose_name='Тип ответа', default='ONE')),
                ('choices_order', models.CharField(choices=[('created', 'В порядке добавления'), ('?', 'В случайном порядке')], max_length=10, verbose_name='Порядок вариантов ответа', default='created')),
                ('voted_users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserHash',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('value', models.BigIntegerField()),
                ('choice', models.ForeignKey(to='polls.Choice')),
                ('user', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, default=None, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('dorm', models.IntegerField(default=0)),
                ('middlename', models.CharField(max_length=100, verbose_name='Отчество', blank=True)),
                ('group', models.CharField(max_length=5, verbose_name='Номер группы', blank=True)),
                ('room', models.CharField(max_length=4, verbose_name='Номер комнаты', blank=True)),
                ('approval', models.BooleanField(verbose_name='Пользователь подтверждён', default=False)),
                ('cardnumber', models.CharField(null=True, max_length=5, verbose_name='Последние пять цифр номера социальной карты', blank=True)),
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
    ]
