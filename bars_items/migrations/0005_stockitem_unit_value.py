# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_items', '0004_auto_20150224_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockitem',
            name='unit_value',
            field=models.FloatField(default=1),
            preserve_default=True,
        ),
    ]
