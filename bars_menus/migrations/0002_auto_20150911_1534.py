# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_items', '0007_auto_20150823_1840'),
        ('bars_menus', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='sellitems',
            field=models.ManyToManyField(to='bars_items.SellItem', through='bars_menus.MenuSellItem'),
        ),
        migrations.AlterField(
            model_name='menusellitem',
            name='menu',
            field=models.ForeignKey(to='bars_menus.Menu'),
        ),
    ]
