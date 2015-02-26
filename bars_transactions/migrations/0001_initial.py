# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('bars_core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bars_items', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountOperation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prev_value', models.FloatField()),
                ('fixed', models.BooleanField(default=False)),
                ('delta', models.FloatField()),
                ('next_value', models.FloatField()),
                ('target', models.ForeignKey(to='bars_core.Account')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ItemOperation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prev_value', models.FloatField()),
                ('fixed', models.BooleanField(default=False)),
                ('delta', models.FloatField()),
                ('next_value', models.FloatField()),
                ('fuzzy', models.BooleanField(default=False)),
                ('target', models.ForeignKey(to='bars_items.StockItem')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=25)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('canceled', models.BooleanField(default=False)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('bar', models.ForeignKey(to='bars_core.Bar')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TransactionData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=128)),
                ('data', models.TextField()),
                ('transaction', models.ForeignKey(to='bars_transactions.Transaction')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='itemoperation',
            name='transaction',
            field=models.ForeignKey(to='bars_transactions.Transaction'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='accountoperation',
            name='transaction',
            field=models.ForeignKey(to='bars_transactions.Transaction'),
            preserve_default=True,
        ),
    ]
