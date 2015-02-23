# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_items', '0002_auto_20150223_0055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockitem',
            name='sellitem',
            field=models.ForeignKey(related_name='stockitems', to='bars_items.SellItem', null=True),
            preserve_default=True,
        ),
    ]
