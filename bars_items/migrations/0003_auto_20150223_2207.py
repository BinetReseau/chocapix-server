# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_items', '0002_stockitem_buy_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='buyitem',
            old_name='item',
            new_name='details',
        ),
        migrations.AlterField(
            model_name='buyitemprice',
            name='price',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
    ]
