# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_base', '0003_auto_20150217_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='name_plural',
            field=models.CharField(max_length=100, blank=True),
            preserve_default=True,
        ),
    ]
