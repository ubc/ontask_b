# Generated by Django 4.2 on 2023-08-10 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ontask', '0068_alter_scheduledoperation_frequency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='athenaconnection',
            name='aws_file_path',
            field=models.CharField(blank=True, default='', max_length=1024, verbose_name='AWS S3 Bucket file path'),
        ),
        migrations.AlterField(
            model_name='athenaconnection',
            name='table_name',
            field=models.CharField(blank=True, default='', help_text='Leave blank to provide at execution', max_length=1024, verbose_name='Table name'),
        ),
        migrations.AlterField(
            model_name='condition',
            name='_formula_text',
            field=models.CharField(blank=True, default='', max_length=2048, verbose_name='formula text'),
        ),
        migrations.AlterField(
            model_name='filter',
            name='_formula_text',
            field=models.CharField(blank=True, default='', max_length=2048, verbose_name='formula text'),
        ),
        migrations.AlterField(
            model_name='sqlconnection',
            name='db_table',
            field=models.CharField(blank=True, default='', help_text='Leave empty to enter at execution', max_length=2048, verbose_name='Database table'),
        ),
    ]