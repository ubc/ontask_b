# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-19 11:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0003_auto_20180530_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]