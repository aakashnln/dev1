# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-17 18:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='client_username',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
