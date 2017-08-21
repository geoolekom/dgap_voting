# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import fin_aid.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AidDocument',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('file', models.FileField(upload_to=fin_aid.models.document_path, verbose_name='Документ')),
            ],
        ),
        migrations.CreateModel(
            name='AidRequest',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('reason', models.TextField(max_length=1024, verbose_name='Причина')),
                ('req_sum', models.FloatField(null=True, blank=True, verbose_name='Запрошенная сумма')),
                ('urgent', models.BooleanField(default=False, verbose_name='Срочно')),
                ('accepted_sum', models.FloatField(null=True, blank=True, verbose_name='Одобренная сумма')),
                ('status', models.IntegerField(choices=[(1, 'Заявление рассматривается'), (2, 'Заявление одобрено'), (3, 'В заявлении отказано'), (4, 'Необходимо уточнить данные')], default=1, verbose_name='Статус заявления')),
                ('add_dttm', models.DateTimeField(auto_now_add=True, verbose_name='Дата подачи')),
                ('examination_dttm', models.DateTimeField(null=True, blank=True, verbose_name='Дата рассмотрения')),
                ('payment_dttm', models.DateTimeField(null=True, blank=True, verbose_name='Дата выплаты')),
                ('examination_comment', models.TextField(null=True, blank=True, verbose_name='Комментарий комиссии')),
                ('submitted_paper', models.BooleanField(default=False, verbose_name='Принес заявление')),
                ('applicant', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('reason', models.CharField(max_length=100, verbose_name='Причина (для заявления)')),
                ('max_sum', models.IntegerField(default=20000, verbose_name='Макс. сумма')),
                ('max_quantity', models.IntegerField(default=1, verbose_name='Макс. раз за семестр')),
            ],
        ),
        migrations.AddField(
            model_name='aidrequest',
            name='category',
            field=models.ForeignKey(to='fin_aid.Category'),
        ),
        migrations.AddField(
            model_name='aiddocument',
            name='request',
            field=models.ForeignKey(to='fin_aid.AidRequest'),
        ),
    ]
