# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-09-30 18:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0005_auto_20170930_1059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.CharField(max_length=255),
        ),
    ]