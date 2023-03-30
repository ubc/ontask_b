# Generated by Django 2.2.24 on 2023-03-30 03:15

from django.db import migrations, models
import django.db.models.deletion

def move_action_reference(apps, schema_editor):
    """Move action reference from field to drop to new field."""

    Action = apps.get_model('ontask', 'Action')
    for aitem in Action.objects.all():
        if aitem.filter:
            aitem.filter_tmp = aitem.filter
            aitem.filter.save()


class Migration(migrations.Migration):

    dependencies = [
        ('ontask', '0039_auto_20230330_1237'),
    ]

    operations = [
        migrations.AddField(
            model_name='filter',
            name='action',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='filter_tmp', to='ontask.Action'),
        ),
	migrations.RunPython(code=move_action_reference),
        migrations.RemoveField(
            model_name='action',
            name='filter',
        ),
        migrations.RemoveField(
            model_name='filter',
            name='action_ref',
        ),
    ]
