# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_base', '0008_item_tax'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='bar',
        ),
        migrations.RemoveField(
            model_name='item',
            name='details',
        ),
        migrations.DeleteModel(
            name='Item',
        ),
        migrations.DeleteModel(
            name='ItemDetails',
        ),
    ]
