# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_menus', '0002_auto_20150911_1534'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menu',
            old_name='sellitems',
            new_name='items',
        ),
    ]
