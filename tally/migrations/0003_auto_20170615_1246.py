# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-15 04:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tally', '0002_auto_20170615_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tally',
            name='pay_type',
            field=models.CharField(choices=[('Income', '收入'), ('Expenses', '支出')], default='收入', max_length=20),
        ),
        migrations.AlterField(
            model_name='tally',
            name='type',
            field=models.CharField(choices=[('Food', '食物'), ('Fun', '玩樂'), ('Traffic', '交通'), ('Other', '其他')], default='其他', max_length=20),
        ),
    ]
