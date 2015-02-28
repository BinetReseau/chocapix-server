# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(max_length=127, choices=[(b'customer', b'customer'), (b'moneymanager', b'moneymanager'), (b'policeman', b'policeman'), (b'admin', b'admin'), (b'inventorymanager', b'inventorymanager'), (b'appromanager', b'appromanager'), (b'newsmanager', b'newsmanager'), (b'accountmanager', b'accountmanager'), (b'agios_daemon', b'agios_daemon'), (b'staff', b'staff')]),
            preserve_default=True,
        ),
        migrations.AlterIndexTogether(
            name='account',
            index_together=set([('bar', 'owner')]),
        ),
    ]
