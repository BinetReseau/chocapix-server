# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_items', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sellitem',
            name='deleted',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stockitem',
            name='deleted',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
