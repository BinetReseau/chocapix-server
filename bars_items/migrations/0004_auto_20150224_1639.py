# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_items', '0003_auto_20150223_2207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sellitem',
            name='unit_value',
        ),
        migrations.AlterField(
            model_name='stockitem',
            name='sellitem',
            field=models.ForeignKey(related_name='stockitems', to='bars_items.SellItem'),
            preserve_default=True,
        ),
    ]
