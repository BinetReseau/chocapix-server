# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_base', '0008_item_tax'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='account',
            index_together=set([('bar', 'owner')]),
        ),
    ]
