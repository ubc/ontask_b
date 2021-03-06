# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-11 05:58
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ontask', '0003_auto_20180116_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='view',
            name='columns',
            field=models.ManyToManyField(related_name='views', to='ontask.Column', verbose_name='Subset of columns to show'),
        ),
        migrations.AlterField(
            model_name='view',
            name='formula',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, help_text='Preselect rows satisfying this condition', null=True, verbose_name='Subset of rows to show'),
        ),
    ]
