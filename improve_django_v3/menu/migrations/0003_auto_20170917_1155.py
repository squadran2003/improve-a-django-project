# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-09-17 18:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_auto_20160406_1554'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menu',
            options={'ordering': ['-expiration_date']},
        ),
    ]