# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-26 19:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apirest', '0002_auto_20171026_1852'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attacheddevices',
            name='name',
        ),
    ]