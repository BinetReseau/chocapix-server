# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_core', '0004_loginattempt_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginattempt',
            name='success',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
