# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-26 19:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apirest_sensehat', '0003_remove_attacheddevices_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='attacheddevices',
            name='name',
            field=models.CharField(default='tutua', max_length=100),
            preserve_default=False,
        ),
    ]
