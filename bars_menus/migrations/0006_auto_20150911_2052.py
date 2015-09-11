# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_menus', '0005_auto_20150911_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menusellitem',
            name='menu',
            field=models.ForeignKey(related_name='items', blank=True, to='bars_menus.Menu'),
        ),
        migrations.AlterField(
            model_name='menusellitem',
            name='sellitem',
            field=models.ForeignKey(to='bars_items.SellItem'),
        ),
    ]
