# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_items', '0005_stockitem_unit_value'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockitem',
            name='buy_price',
        ),
    ]
