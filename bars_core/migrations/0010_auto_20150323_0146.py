# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_core', '0009_bar_agios_enabled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(max_length=127, choices=[(b'customer', b'customer'), (b'moneymanager', b'moneymanager'), (b'policeman', b'policeman'), (b'admin', b'admin'), (b'itemmanager', b'itemmanager'), (b'appromanager', b'appromanager'), (b'barmanager', b'barmanager'), (b'usermanager', b'usermanager'), (b'newsmanager', b'newsmanager'), (b'treasurer', b'treasurer'), (b'stockmanager', b'stockmanager'), (b'inventorymanager', b'inventorymanager'), (b'accountmanager', b'accountmanager'), (b'agios_daemon', b'agios_daemon'), (b'staff', b'staff')]),
            preserve_default=True,
        ),
    ]
