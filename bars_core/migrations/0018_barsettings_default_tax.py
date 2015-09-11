# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_core', '0017_auto_20150726_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='barsettings',
            name='default_tax',
            field=models.FloatField(default=0.2),
        ),
    ]
