# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-25 07:28
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ontask', '0014_auto_20180730_1921'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduledemailaction',
            name='exclude_values',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list, null=True, verbose_name='payload'),
        ),
    ]
