# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_api', '0004_auto_20150114_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountoperation',
            name='delta',
            field=models.DecimalField(max_digits=8, decimal_places=3),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='itemoperation',
            name='delta',
            field=models.FloatField(),
            preserve_default=True,
        ),
    ]
