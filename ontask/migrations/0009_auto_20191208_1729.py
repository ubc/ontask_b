# Generated by Django 2.2.8 on 2019-12-08 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ontask', '0008_auto_20191208_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduledoperation',
            name='execute_until',
            field=models.DateTimeField(blank=True, null=True, verbose_name='End of execution period (Optional)'),
        ),
    ]
