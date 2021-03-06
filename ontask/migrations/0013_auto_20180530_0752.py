# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-29 22:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ontask', '0012_sqlconnection'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sqlconnection',
            old_name='conn_type',
            new_name='Connection type',
        ),
        migrations.RenameField(
            model_name='sqlconnection',
            old_name='db_name',
            new_name='DB name',
        ),
        migrations.RenameField(
            model_name='sqlconnection',
            old_name='description_text',
            new_name='Description',
        ),
        migrations.RenameField(
            model_name='sqlconnection',
            old_name='db_host',
            new_name='Host',
        ),
        migrations.RenameField(
            model_name='sqlconnection',
            old_name='db_password',
            new_name='Password',
        ),
        migrations.RenameField(
            model_name='sqlconnection',
            old_name='ncols',
            new_name='Port',
        ),
        migrations.RenameField(
            model_name='sqlconnection',
            old_name='db_user',
            new_name='User name',
        ),
    ]
