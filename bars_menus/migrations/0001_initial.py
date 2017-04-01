# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_items', '0007_auto_20150823_1840'),
        ('bars_core', '0018_barsettings_default_tax'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('account', models.ForeignKey(to='bars_core.Account')),
            ],
        ),
        migrations.CreateModel(
            name='MenuSellItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('qty', models.FloatField(default=0)),
                ('menu', models.ForeignKey(to='bars_menus.Menu', blank=True)),
                ('sellitem', models.ForeignKey(to='bars_items.SellItem')),
            ],
        ),
    ]
