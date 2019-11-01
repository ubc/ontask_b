# Generated by Django 2.2 on 2019-04-18 06:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ontask', '0030_remove_workflow_lusers'),
    ]

    operations = [
        migrations.AddField(
            model_name='workflow',
            name='lusers',
            field=models.ManyToManyField(related_name='workflows_luser', to=settings.AUTH_USER_MODEL),
        ),
    ]