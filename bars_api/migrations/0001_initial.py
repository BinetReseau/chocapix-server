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
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('username', models.CharField(unique=True, max_length=128)),
                ('full_name', models.CharField(max_length=128, blank=True)),
                ('pseudo', models.CharField(max_length=128, blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('money', models.FloatField(default=0)),
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
                ('prev_value', models.FloatField()),
                ('fixed', models.BooleanField(default=False)),
                ('delta', models.FloatField()),
                ('next_value', models.FloatField()),
                ('target', models.ForeignKey(to='bars_api.Account')),
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
                ('keywords', models.CharField(max_length=200, blank=True)),
                ('qty', models.FloatField(default=0)),
                ('unit', models.CharField(max_length=100, blank=True)),
                ('unit_value', models.FloatField(default=1)),
                ('buy_unit', models.CharField(max_length=100, blank=True)),
                ('buy_unit_value', models.FloatField(default=1)),
                ('price', models.FloatField()),
                ('buy_price', models.FloatField(default=1)),
                ('deleted', models.BooleanField(default=False)),
                ('unavailable', models.BooleanField(default=False)),
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
                ('fixed', models.BooleanField(default=False)),
                ('delta', models.FloatField()),
                ('next_value', models.FloatField()),
                ('target', models.ForeignKey(to='bars_api.Item')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('text', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('bar', models.ForeignKey(to='bars_api.Bar')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=127)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('bar', models.ForeignKey(to='bars_api.Bar')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
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
