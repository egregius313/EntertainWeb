# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-20 02:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lights', '0010_accesstoken_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='button',
            name='svg_image',
            field=models.CharField(default='none', max_length=256),
        ),
    ]