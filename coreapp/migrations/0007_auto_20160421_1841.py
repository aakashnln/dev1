# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-21 13:11
from __future__ import unicode_literals

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0006_auto_20160421_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientcampaigndetail',
            name='daily_earning_max',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='clientcampaigndetail',
            name='daily_earning_min',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='clientcampaigndetail',
            name='wrap_type',
            field=models.CharField(choices=[(b'1', b'Full'), (b'2', b'Partial'), (b'3', b'Panel'), (b'4', b'Unknown')], default=b'4', max_length=1),
        ),
        migrations.AlterField(
            model_name='clientcampaign',
            name='wrap_type',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(b'1', b'Full'), (b'2', b'Partial'), (b'3', b'Panel'), (b'4', b'Unknown')], default=b'4', max_length=1),
        ),
    ]