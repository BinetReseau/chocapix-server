# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(unique=True, max_length=128)),
                ('password', models.CharField(unique=True, max_length=128)),
                ('full_name', models.CharField(max_length=128, blank=True)),
                ('pseudo', models.CharField(max_length=128, blank=True)),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('money', models.DecimalField(max_digits=8, decimal_places=3)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AccountOperation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prev_value', models.DecimalField(max_digits=8, decimal_places=3)),
                ('delta', models.DecimalField(max_digits=8, decimal_places=3)),
                ('account', models.ForeignKey(to='bars_api.Account')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Bar',
            fields=[
                ('id', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('keywords', models.CharField(max_length=200)),
                ('qty', models.FloatField()),
                ('unit', models.CharField(max_length=100, blank=True)),
                ('unit_value', models.FloatField(default=1)),
                ('buy_unit', models.CharField(max_length=100, blank=True)),
                ('buy_unit_value', models.FloatField(default=1)),
                ('price', models.FloatField()),
                ('buy_price', models.FloatField(default=1)),
                ('deleted', models.BooleanField(default=False)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('bar', models.ForeignKey(to='bars_api.Bar')),
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
                ('delta', models.FloatField()),
                ('item', models.ForeignKey(to='bars_api.Item')),
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
                ('bar', models.ForeignKey(to='bars_api.Bar')),
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
                ('transaction', models.ForeignKey(to='bars_api.Transaction')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='itemoperation',
            name='transaction',
            field=models.ForeignKey(to='bars_api.Transaction'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='accountoperation',
            name='transaction',
            field=models.ForeignKey(to='bars_api.Transaction'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='bar',
            field=models.ForeignKey(to='bars_api.Bar'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='account',
            unique_together=set([('bar', 'owner')]),
        ),
    ]
