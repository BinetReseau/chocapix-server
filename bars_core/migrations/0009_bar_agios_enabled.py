# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_core', '0008_bar_agios_factor'),
    ]

    operations = [
        migrations.AddField(
            model_name='bar',
            name='agios_enabled',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
