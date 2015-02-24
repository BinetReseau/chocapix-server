# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_items', '0007_auto_20150224_1910'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemdetails',
            name='unit_name',
        ),
        migrations.RemoveField(
            model_name='itemdetails',
            name='unit_name_plural',
        ),
    ]
