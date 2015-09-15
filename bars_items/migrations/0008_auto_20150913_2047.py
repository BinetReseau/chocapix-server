# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_items', '0007_auto_20150823_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockitem',
            name='last_inventory',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
