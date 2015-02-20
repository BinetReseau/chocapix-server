# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars_base', '0006_account_deleted'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('barcode', models.CharField(max_length=25, blank=True)),
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
        migrations.RemoveField(
            model_name='item',
            name='buy_unit_name',
        ),
        migrations.RemoveField(
            model_name='item',
            name='buy_unit_name_plural',
        ),
        migrations.RemoveField(
            model_name='item',
            name='buy_unit_value',
        ),
        migrations.RemoveField(
            model_name='item',
            name='keywords',
        ),
        migrations.RemoveField(
            model_name='item',
            name='name',
        ),
        migrations.RemoveField(
            model_name='item',
            name='name_plural',
        ),
        migrations.AddField(
            model_name='item',
            name='details',
            field=models.ForeignKey(default=None, to='bars_base.ItemDetails'),
            preserve_default=False,
        ),
    ]
