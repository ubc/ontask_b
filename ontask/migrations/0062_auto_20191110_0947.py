# Generated by Django 2.2.6 on 2019-11-09 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ontask', '0061_auto_20191104_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduledoperation',
            name='operation_type',
            field=models.CharField(choices=[('run_action_personalized_text', 'Run personalized text action'), ('run_action_personalized_json', 'Run personalized JSON action'), ('run_action_send_list', 'Run send list action'), ('run_action_send_list_json', 'Run send JSON list action'), ('run_action_rubric_text', 'Run rubrict text action')], max_length=512),
        ),
    ]
