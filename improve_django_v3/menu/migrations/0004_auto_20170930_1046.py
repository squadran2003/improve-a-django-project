# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-09-30 17:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_auto_20170917_1155'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menu',
            options={},
        ),
        migrations.AlterField(
            model_name='menu',
            name='items',
            field=models.ManyToManyField(related_name='item', to='menu.Item'),
        ),
    ]
