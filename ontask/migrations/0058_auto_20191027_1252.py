# Generated by Django 2.2.6 on 2019-10-27 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ontask', '0057_auto_20191026_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduledoperation',
            name='operation_type',
            field=models.CharField(choices=[('run_action', 'Run action')], max_length=512),
        ),
    ]
