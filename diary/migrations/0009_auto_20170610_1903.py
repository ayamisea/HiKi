# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-10 11:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0008_auto_20170609_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='description',
            field=models.CharField(blank=True, max_length=96, null=True),
        ),
    ]