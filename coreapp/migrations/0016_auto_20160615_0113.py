# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-14 19:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0015_auto_20160612_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drivercampaign',
            name='end_date',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='drivercampaign',
            name='start_date',
            field=models.DateTimeField(blank=True),
        ),
    ]
