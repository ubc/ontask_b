# Generated by Django 2.1.7 on 2019-02-28 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ontask', '0024_auto_20180925_1934'),
        ('ontask', '0048_auto_20190228_1952'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ColumnConditionPair',
            new_name='ActionColumnConditionTuple',
        ),
    ]
