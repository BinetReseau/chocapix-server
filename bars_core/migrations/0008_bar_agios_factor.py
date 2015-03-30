# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_core', '0007_bar_agios_threshold'),
    ]

    operations = [
        migrations.AddField(
            model_name='bar',
            name='agios_factor',
            field=models.FloatField(default=0.05),
            preserve_default=True,
        ),
    ]
