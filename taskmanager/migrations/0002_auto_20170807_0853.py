# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-07 08:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='availability',
            old_name='endingTime',
            new_name='endingAvailableTime',
        ),
        migrations.AddField(
            model_name='availability',
            name='totalWeight',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='availability',
            name='used',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='weeklyschedule',
            name='totalWeight',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='task',
            name='type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='taskmanager.TaskTypeWeight'),
        ),
        migrations.AlterField(
            model_name='weeklyschedule',
            name='duration',
            field=models.DurationField(),
        ),
    ]
