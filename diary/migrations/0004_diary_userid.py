# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-06 05:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('diary', '0003_remove_diary_userid'),
    ]

    operations = [
        migrations.AddField(
            model_name='diary',
            name='userID',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
