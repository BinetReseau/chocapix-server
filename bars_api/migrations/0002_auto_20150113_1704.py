# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='unavailable',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='money',
            field=models.FloatField(),
            preserve_default=True,
        ),
    ]
