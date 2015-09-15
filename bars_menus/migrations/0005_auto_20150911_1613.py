# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_menus', '0004_auto_20150911_1600'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='items',
        ),
        migrations.AlterField(
            model_name='menusellitem',
            name='menu',
            field=models.ForeignKey(related_name='menu_sellitems', blank=True, to='bars_menus.Menu'),
        ),
        migrations.AlterField(
            model_name='menusellitem',
            name='sellitem',
            field=models.ForeignKey(related_name='menu_sellitems', to='bars_items.SellItem'),
        ),
    ]
