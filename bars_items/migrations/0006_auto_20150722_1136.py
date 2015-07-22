# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('bars_items', '0005_stockitem_last_inventory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockitem',
            name='last_inventory',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 24, 21, 17, 0, 0, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
