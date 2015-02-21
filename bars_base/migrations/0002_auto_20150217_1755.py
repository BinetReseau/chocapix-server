# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_base', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='buy_unit',
            new_name='buy_unit_name',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='unit',
            new_name='unit_name',
        ),
    ]
