# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_base', '0002_auto_20150217_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='buy_unit_name_plural',
            field=models.CharField(max_length=100, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='name_plural',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='unit_name_plural',
            field=models.CharField(max_length=100, blank=True),
            preserve_default=True,
        ),
    ]
