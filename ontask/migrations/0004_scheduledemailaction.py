# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-16 08:54
from __future__ import unicode_literals

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ontask', '0013_auto_20171209_0809'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ontask', '0008_auto_20171209_1808'),
        ('ontask', '0003_auto_20171216_1944'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduledEmailAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=256)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('execute', models.DateTimeField(null=True)),
                ('status', models.IntegerField(choices=[(0, 'pending'), (1, 'running'), (2, 'done')], verbose_name='Execution Status')),
                ('subject', models.CharField(blank=True, default='', max_length=2048, verbose_name='Email subject')),
                ('send_confirmation', models.BooleanField(default=False, verbose_name='Send you a confirmation email')),
                ('track_read', models.BooleanField(default=False, verbose_name='Track if emails are read?')),
                ('add_column', models.BooleanField(default=False, verbose_name='Add a column with the number of email reads tracked')),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scheduled_actions', to='ontask.Action')),
                ('email_column', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, to='ontask.Column', verbose_name='Column containing the email address')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('workflow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scheduled_actions', to='ontask.Workflow')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]