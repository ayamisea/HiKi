# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-19 03:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tally', '0014_auto_20170619_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tally',
            name='type',
            field=models.CharField(choices=[('收入', (('打工', '打工'), ('零用錢', '零用錢'), ('其他收入', '其他收入'))), ('支出', (('食物', '食物'), ('玩樂', '玩樂'), ('交通', '交通'), ('其他支出', '其他支出')))], max_length=20),
        ),
    ]
