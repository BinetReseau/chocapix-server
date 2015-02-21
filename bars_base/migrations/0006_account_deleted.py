# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_base', '0005_remove_item_unavailable'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='deleted',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
