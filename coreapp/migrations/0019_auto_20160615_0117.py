# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-14 19:47
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0018_auto_20160615_0116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drivercampaign',
            name='end_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2016, 6, 15, 1, 17, 40, 82388)),
        ),
        migrations.AlterField(
            model_name='drivercampaign',
            name='start_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2016, 6, 15, 1, 17, 40, 82363)),
        ),
    ]
