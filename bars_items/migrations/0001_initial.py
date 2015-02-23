# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_core', '0005_user_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('barcode', models.CharField(max_length=25, blank=True)),
                ('itemqty', models.FloatField(default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BuyItemPrice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.FloatField(default=1)),
                ('bar', models.ForeignKey(to='bars_core.Bar')),
                ('buyitem', models.ForeignKey(to='bars_items.BuyItem')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ItemDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('name_plural', models.CharField(max_length=100, blank=True)),
                ('keywords', models.CharField(max_length=200, blank=True)),
                ('unit_name', models.CharField(max_length=100, blank=True)),
                ('unit_name_plural', models.CharField(max_length=100, blank=True)),
                ('unit_value', models.FloatField(default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SellItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('name_plural', models.CharField(max_length=100, blank=True)),
                ('unit_name', models.CharField(max_length=100, blank=True)),
                ('unit_name_plural', models.CharField(max_length=100, blank=True)),
                ('unit_value', models.FloatField(default=1)),
                ('tax', models.FloatField(default=0)),
                ('bar', models.ForeignKey(to='bars_core.Bar')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StockItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('qty', models.FloatField(default=0)),
                ('price', models.FloatField()),
                ('bar', models.ForeignKey(to='bars_core.Bar')),
                ('details', models.ForeignKey(to='bars_items.ItemDetails')),
                ('sellitem', models.ForeignKey(related_name='stockitems', to='bars_items.SellItem')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='stockitem',
            unique_together=set([('bar', 'details')]),
        ),
        migrations.AlterUniqueTogether(
            name='buyitemprice',
            unique_together=set([('bar', 'buyitem')]),
        ),
        migrations.AddField(
            model_name='buyitem',
            name='item',
            field=models.ForeignKey(to='bars_items.ItemDetails'),
            preserve_default=True,
        ),
    ]
