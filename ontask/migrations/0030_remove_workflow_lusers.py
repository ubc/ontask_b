# Generated by Django 2.2 on 2019-04-18 06:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ontask', '0029_auto_20190418_1554'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workflow',
            name='lusers',
        ),
    ]
