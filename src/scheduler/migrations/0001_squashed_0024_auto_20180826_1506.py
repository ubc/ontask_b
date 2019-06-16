# Generated by Django 2.2.1 on 2019-05-24 02:13

import django.contrib.postgres.fields.jsonb
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# scheduler.migrations.0017_auto_20180826_1409
def reassign_email_to_item(apps, schema_editor):
    if schema_editor.connection.alias != 'default':
        return

    # Traverse the scheduled actions and move the value from email_column to
    # item_column
    ScheduledEmailAction = apps.get_model('scheduler', 'ScheduledEmailAction')
    for item in ScheduledEmailAction.objects.all():
        item.item_column = item.email_column
        item.save()

# scheduler.migrations.0024_auto_20180826_1506
def combine_fields_into_payload(apps, schema_editor):
    if schema_editor.connection.alias != 'default':
        return

    # Traverse the scheduled actions and move the value from email_column to
    # item_column
    ScheduledAction = apps.get_model('scheduler', 'ScheduledAction')
    for item in ScheduledAction.objects.all():
        payload = {}
        payload['subject'] = item.subject
        if item.cc_email:
            payload['cc_email'] = item.cc_email
        if item.bcc_email:
            payload['bcc_email'] = item.bcc_email
        payload['send_confirmation'] = item.send_confirmation
        payload['track_read'] = item.track_read
        item.payload = payload
        item.save()


class Migration(migrations.Migration):

    replaces = [('scheduler', '0001_initial'), ('scheduler', '0002_auto_20171216_1904'), ('scheduler', '0003_auto_20171216_1944'), ('scheduler', '0004_scheduledemailaction'), ('scheduler', '0005_auto_20171218_0045'), ('scheduler', '0006_auto_20171218_0057'), ('scheduler', '0007_auto_20171218_0100'), ('scheduler', '0008_remove_scheduledemailaction_workflow'), ('scheduler', '0009_auto_20171218_2125'), ('scheduler', '0010_scheduledemailaction_message'), ('scheduler', '0011_scheduledemailaction_deleted'), ('scheduler', '0012_remove_scheduledemailaction_add_column'), ('scheduler', '0013_auto_20180730_1918'), ('scheduler', '0014_auto_20180730_1921'), ('scheduler', '0015_scheduledemailaction_exclude_values'), ('scheduler', '0016_auto_20180826_1408'), ('scheduler', '0017_auto_20180826_1409'), ('scheduler', '0018_auto_20180826_1414'), ('scheduler', '0019_auto_20180826_1431'), ('scheduler', '0020_auto_20180826_1433'), ('scheduler', '0021_auto_20180826_1458'), ('scheduler', '0022_auto_20180826_1503'), ('scheduler', '0023_auto_20180826_1505'), ('scheduler', '0024_auto_20180826_1506')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('action', '0008_auto_20171209_1808'),
        ('workflow', '0013_auto_20171209_0809'),
        ('workflow', '0023_auto_20180722_1013'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduledEmailAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=256)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('execute', models.DateTimeField(verbose_name='When to execute this action')),
                ('status', models.IntegerField(choices=[(0, 'pending'), (1, 'running'), (2, 'done'), (3, 'done_error')], verbose_name='Execution Status')),
                ('subject', models.CharField(default='', max_length=2048, verbose_name='Email subject')),
                ('send_confirmation', models.BooleanField(default=False, verbose_name='Send you a confirmation email')),
                ('track_read', models.BooleanField(default=False, verbose_name='Track if emails are read?')),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scheduled_actions', to='action.Action')),
                ('email_column', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, related_name='scheduled_email_actions', to='workflow.Column', verbose_name='Column to select the elements for the action')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('message', models.TextField(blank=True, verbose_name='Execution message')),
                ('deleted', models.BooleanField(default=False)),
                ('bcc_email', models.CharField(blank=True, default='', max_length=2048, verbose_name='Comma-separated list of BCC Emails')),
                ('cc_email', models.CharField(blank=True, default='', max_length=2048, verbose_name='Comma-separated list of CC Emails')),
                ('exclude_values', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list, null=True, verbose_name='payload')),
                ('item_column', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scheduled_actions', to='workflow.Column', verbose_name='Column to select the elements for the action')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RunPython(code=reassign_email_to_item),
        migrations.RemoveField(
            model_name='scheduledemailaction',
            name='email_column',
        ),
        migrations.AlterField(
            model_name='scheduledemailaction',
            name='item_column',
            field=models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, related_name='scheduled_actions', to='workflow.Column', verbose_name='Column to select the elements for the action'),
        ),
        migrations.AlterField(
            model_name='scheduledemailaction',
            name='type',
            field=models.CharField(choices=[('email_send', 'Send emails')], max_length=256),
        ),
        migrations.AlterField(
            model_name='scheduledemailaction',
            name='status',
            field=models.CharField(choices=[('creating', 'Creating'), ('pending', 'Pencding'), ('executing', 'Executing'), ('done', 'Finished'), ('done_error', 'Finished with error')], max_length=256, verbose_name='Execution Status'),
        ),
        migrations.AlterField(
            model_name='scheduledemailaction',
            name='status',
            field=models.CharField(choices=[('creating', 'Creating'), ('pending', 'Pending'), ('executing', 'Executing'), ('done', 'Finished'), ('done_error', 'Finished with error')], max_length=256, verbose_name='Execution Status'),
        ),
        migrations.RenameModel(
            old_name='ScheduledEmailAction',
            new_name='ScheduledAction',
        ),
        migrations.AddField(
            model_name='scheduledaction',
            name='payload',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list, null=True, verbose_name='payload'),
        ),
        migrations.AlterField(
            model_name='scheduledaction',
            name='exclude_values',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list, null=True, verbose_name='exclude values'),
        ),
        migrations.RunPython(code=combine_fields_into_payload),
    ]