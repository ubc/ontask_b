# Generated by Django 2.2.6 on 2019-10-27 07:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ontask', '0058_auto_20191027_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduledoperation',
            name='action',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scheduled_operations', to='ontask.Action'),
        ),
        migrations.AlterField(
            model_name='scheduledoperation',
            name='workflow',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scheduled_operations', to='ontask.Workflow'),
        ),
    ]