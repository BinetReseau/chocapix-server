# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_items', '0001_initial'),
        ('bars_transactions', '0002_remove_itemoperation_target'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemoperation',
            name='target',
            field=models.ForeignKey(default=None, to='bars_items.StockItem'),
            preserve_default=False,
        ),
    ]
