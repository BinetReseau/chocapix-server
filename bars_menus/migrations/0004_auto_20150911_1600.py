# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_menus', '0003_auto_20150911_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menusellitem',
            name='menu',
            field=models.ForeignKey(to='bars_menus.Menu', blank=True),
        ),
    ]
