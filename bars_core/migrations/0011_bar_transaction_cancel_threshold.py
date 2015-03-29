# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_core', '0010_auto_20150323_0146'),
    ]

    operations = [
        migrations.AddField(
            model_name='bar',
            name='transaction_cancel_threshold',
            field=models.FloatField(default=48),
            preserve_default=True,
        ),
    ]
