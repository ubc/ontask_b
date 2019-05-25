# Generated by Django 2.2.1 on 2019-05-23 23:16

import django.contrib.postgres.fields.jsonb
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

from dataops.pandas import load_table

# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# workflow.migrations.0022_auto_20180510_1157

def forwards(apps, schema_editor):
    if schema_editor.connection.alias != 'default':
        return
    # Traverse the workflows and verify that the columns are in the same
    # order than the columns in the workflow
    Workflow = apps.get_model('workflow', 'Workflow')

    for w in Workflow.objects.all():
        if not w.is_table_in_db(w):
            continue

        df = load_table(w.id)

        if len(df.columns) != w.ncols:
            raise Exception('Inconsistent number of columns')

        df_columns = list(df.columns)
        for c in w.columns.all():
            c.position = df_columns.index(c.name) + 1
            c.save()


class Migration(migrations.Migration):

    replaces = [('workflow', '0001_initial'), ('workflow', '0002_auto_20171110_2300'), ('workflow', '0003_workflow_shared'), ('workflow', '0004_column_description_text'), ('workflow', '0005_auto_20171125_2049'), ('workflow', '0006_auto_20171125_2052'), ('workflow', '0007_auto_20171208_2133'), ('workflow', '0008_auto_20171208_2139'), ('workflow', '0009_auto_20171208_2307'), ('workflow', '0010_auto_20171208_2326'), ('workflow', '0011_auto_20171208_2327'), ('workflow', '0012_auto_20171208_2328'), ('workflow', '0013_auto_20171209_0809'), ('workflow', '0014_column_in_viz'), ('workflow', '0015_auto_20180408_0910'), ('workflow', '0016_auto_20180409_0826'), ('workflow', '0017_auto_20180417_1557'), ('workflow', '0018_auto_20180428_1425'), ('workflow', '0019_auto_20180428_1606'), ('workflow', '0020_auto_20180429_1139'), ('workflow', '0021_auto_20180429_1157'), ('workflow', '0022_auto_20180510_1157'), ('workflow', '0023_auto_20180722_1013'), ('workflow', '0024_auto_20180925_1934')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Workflow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
                ('description_text', models.CharField(blank=True, default='', max_length=2048)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('nrows', models.IntegerField(blank=True, default=0, verbose_name='Number of rows')),
                ('ncols', models.IntegerField(blank=True, default=0, verbose_name='Number of columns')),
                ('attributes', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True)),
                ('query_builder_ops', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True)),
                ('data_frame_table_name', models.CharField(blank=True, default='', max_length=1024)),
                ('session_key', models.CharField(blank=True, default='', max_length=40)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('shared', models.ManyToManyField(related_name='shared_workflows', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, verbose_name='Column name')),
                ('data_type', models.CharField(choices=[('boolean', 'boolean'), ('datetime', 'datetime'), ('string', 'string'), ('integer', 'integer'), ('double', 'double')], max_length=512, verbose_name='Type of data to store in the column')),
                ('is_key', models.BooleanField(default=False, verbose_name='Has unique values per row')),
                ('categories', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list, null=True, verbose_name='Comma separated list of values allowed in this column')),
                ('workflow', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='columns', to='workflow.Workflow')),
                ('description_text', models.CharField(blank=True, default='', max_length=2048, verbose_name='Description')),
                ('active_from', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Column active from')),
                ('active_to', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Column active until')),
                ('in_viz', models.BooleanField(default=True, verbose_name='Include in visualization')),
                ('position', models.IntegerField(default=0, verbose_name='Column position (zero to insert last)')),
            ],
            options={
                'ordering': ('position',),
                'unique_together': {('name', 'workflow')},
            },
        ),
        migrations.RunPython(forwards),
        migrations.AlterModelOptions(
            name='column',
            options={'ordering': ('position',), 'verbose_name': 'column', 'verbose_name_plural': 'columns'},
        ),
        migrations.AlterModelOptions(
            name='workflow',
            options={'verbose_name': 'workflow', 'verbose_name_plural': 'workflows'},
        ),
        migrations.AlterField(
            model_name='column',
            name='categories',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list, null=True, verbose_name='comma separated list of values allowed'),
        ),
        migrations.AlterField(
            model_name='column',
            name='data_type',
            field=models.CharField(choices=[('boolean', 'boolean'), ('datetime', 'datetime'), ('string', 'string'), ('integer', 'integer'), ('double', 'double')], max_length=512, verbose_name='type of data to store in the column'),
        ),
        migrations.AlterField(
            model_name='column',
            name='description_text',
            field=models.CharField(blank=True, default='', max_length=2048, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='column',
            name='in_viz',
            field=models.BooleanField(default=True, verbose_name='include in visualization'),
        ),
        migrations.AlterField(
            model_name='column',
            name='is_key',
            field=models.BooleanField(default=False, verbose_name='has unique values per row'),
        ),
        migrations.AlterField(
            model_name='column',
            name='name',
            field=models.CharField(max_length=512, verbose_name='column name'),
        ),
        migrations.AlterField(
            model_name='column',
            name='position',
            field=models.IntegerField(default=0, verbose_name='column position (zero to insert last)'),
        ),
        migrations.AlterField(
            model_name='workflow',
            name='ncols',
            field=models.IntegerField(blank=True, default=0, verbose_name='number of columns'),
        ),
        migrations.AlterField(
            model_name='workflow',
            name='nrows',
            field=models.IntegerField(blank=True, default=0, verbose_name='number of rows'),
        ),
        migrations.AlterField(
            model_name='column',
            name='data_type',
            field=models.CharField(choices=[('string', 'string'), ('integer', 'integer'), ('double', 'double'), ('boolean', 'boolean'), ('datetime', 'datetime')], max_length=512, verbose_name='type of data to store in the column'),
        ),
    ]
