# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-16 16:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lights', '0002_button_related_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='button',
            name='button_name',
            field=models.CharField(default='', max_length=8),
        ),
    ]