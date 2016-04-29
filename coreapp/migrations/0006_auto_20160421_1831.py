# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-21 13:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0005_clientcampaign_campaign_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientCampaignDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monthly_cap', models.FloatField(default=0.0)),
                ('monthly_km_cap', models.FloatField(default=0.0)),
            ],
        ),
        migrations.AddField(
            model_name='clientcampaign',
            name='wrap_type',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(b'1', b'Full'), (b'2', b'Partial'), (b'3', b'Panel')], default=b'4', max_length=1),
        ),
        migrations.AlterField(
            model_name='clientcampaign',
            name='campaign_status',
            field=models.CharField(choices=[(b'1', b'New'), (b'2', b'Processing'), (b'3', b'Active'), (b'4', b'Closed'), (b'5', b'Unknown')], default=b'4', max_length=1),
        ),
        migrations.AddField(
            model_name='clientcampaigndetail',
            name='campaign',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coreapp.ClientCampaign'),
        ),
    ]
