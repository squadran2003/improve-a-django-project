# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-09-30 17:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_auto_20170930_1046'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menu',
            options={'ordering': ['-created_date']},
        ),
    ]
