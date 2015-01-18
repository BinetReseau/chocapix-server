# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_api', '0006_news'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountoperation',
            name='next_value',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='itemoperation',
            name='next_value',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='accountoperation',
            name='delta',
            field=models.FloatField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='accountoperation',
            name='prev_value',
            field=models.FloatField(),
            preserve_default=True,
        ),
    ]
