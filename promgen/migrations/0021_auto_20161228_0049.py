# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-28 00:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


def convert_to_project(apps, schema_editor):
    Sender = apps.get_model('promgen', 'Sender')
    Project = apps.get_model('promgen', 'Project')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    project_type = ContentType.objects.get_for_model(Project)

    for sender in Sender.objects.all():
        if sender.content_type_id == project_type.id:
            sender.project_id = sender.object_id
            sender.save()
        else:
            sender.delete()


def convert_to_content_type(apps, schema_editor):
    Sender = apps.get_model('promgen', 'Sender')
    Project = apps.get_model('promgen', 'Project')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    project_type = ContentType.objects.get_for_model(Project)
    for sender in Sender.objects.all():
        sender.object_id = sender.project_id
        sender.content_type_id = project_type.id
        sender.save()


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('promgen', '0020_auto_20161226_0337'),
    ]

    operations = [
        migrations.AddField(
            model_name='sender',
            name='content_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sender',
            name='object_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.RunPython(convert_to_content_type, convert_to_project),
        migrations.RemoveField(
            model_name='sender',
            name='project',
        ),
    ]