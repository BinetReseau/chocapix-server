# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_core', '0006_account_overdrawn_since'),
    ]

    operations = [
        migrations.AddField(
            model_name='bar',
            name='agios_threshold',
            field=models.FloatField(default=2),
            preserve_default=True,
        ),
    ]
