# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-08 06:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ses', '0002_scorerule_createteacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='groupid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='isHeadman',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
