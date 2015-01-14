# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_api', '0002_auto_20150113_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemoperation',
            name='delta',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
    ]
