# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_base', '0007_auto_20150218_1931'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='tax',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
    ]
