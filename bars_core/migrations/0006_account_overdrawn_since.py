# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_core', '0005_auto_20150303_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='overdrawn_since',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
    ]
