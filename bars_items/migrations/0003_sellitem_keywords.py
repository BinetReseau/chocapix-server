# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_items', '0002_remove_itemdetails_unit_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='sellitem',
            name='keywords',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
    ]
