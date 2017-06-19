# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-19 02:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tally', '0008_auto_20170619_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tally',
            name='pay_type',
            field=models.CharField(choices=[('收入', '收入'), ('支出', '支出')], default='收入', max_length=20),
        ),
        migrations.AlterField(
            model_name='tally',
            name='type',
            field=models.CharField(max_length=20),
        ),
    ]