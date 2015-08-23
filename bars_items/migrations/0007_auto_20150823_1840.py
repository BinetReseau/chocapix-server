# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_items', '0006_auto_20150725_1409'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemdetails',
            name='ranking_unit',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='itemdetails',
            name='ranking_unit_factor',
            field=models.FloatField(default=1),
        ),
    ]
