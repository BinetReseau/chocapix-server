# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_base', '0004_auto_20150218_0257'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='unavailable',
        ),
    ]
