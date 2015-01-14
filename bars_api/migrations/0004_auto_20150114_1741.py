# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_api', '0003_auto_20150114_1633'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accountoperation',
            old_name='account',
            new_name='target',
        ),
        migrations.RenameField(
            model_name='itemoperation',
            old_name='item',
            new_name='target',
        ),
        migrations.AddField(
            model_name='accountoperation',
            name='fixed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='itemoperation',
            name='fixed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='accountoperation',
            name='delta',
            field=models.DecimalField(null=True, max_digits=8, decimal_places=3),
            preserve_default=True,
        ),
    ]
