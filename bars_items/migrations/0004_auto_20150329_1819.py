# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_items', '0003_sellitem_keywords'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemdetails',
            name='brand',
            field=models.CharField(max_length=100, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='itemdetails',
            name='container',
            field=models.CharField(max_length=100, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='itemdetails',
            name='container_plural',
            field=models.CharField(max_length=100, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='itemdetails',
            name='container_qty',
            field=models.FloatField(default=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='itemdetails',
            name='unit',
            field=models.CharField(max_length=100, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='itemdetails',
            name='unit_plural',
            field=models.CharField(max_length=100, blank=True),
            preserve_default=True,
        ),
    ]
