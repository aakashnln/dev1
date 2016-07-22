# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-20 15:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0003_auto_20160419_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientcampaign',
            name='campaign_status',
            field=models.CharField(choices=[(b'1', b'New'), (b'2', b'Processing'), (b'3', b'Active'), (b'5', b'Closed'), (b'4', b'Unknown')], default=b'4', max_length=1),
        ),
    ]