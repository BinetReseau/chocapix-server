# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_items', '0006_remove_stockitem_buy_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stockitem',
            old_name='unit_value',
            new_name='unit_factor',
        ),
    ]
