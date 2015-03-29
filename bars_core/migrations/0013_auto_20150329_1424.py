# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def migrate_barsettings(apps, schema_editor):
    Bar = apps.get_model("bars_core", "Bar")
    BarSettings = apps.get_model("bars_core", "BarSettings")
    for bar in Bar.objects.all():
        settings, _ = BarSettings.objects.get_or_create(bar=bar)
        settings.next_scheduled_appro = bar.next_scheduled_appro
        settings.money_warning_threshold = bar.money_warning_threshold
        settings.transaction_cancel_threshold = bar.transaction_cancel_threshold
        settings.agios_enabled = bar.agios_enabled
        settings.agios_threshold = bar.agios_threshold
        settings.agios_factor = bar.agios_factor
        settings.save()


class Migration(migrations.Migration):

    dependencies = [
        ('bars_core', '0012_auto_20150328_2317'),
    ]

    operations = [
        migrations.CreateModel(
            name='BarSettings',
            fields=[
                ('bar', models.OneToOneField(related_name='settings', primary_key=True, serialize=False, to='bars_core.Bar')),
                ('next_scheduled_appro', models.DateTimeField(null=True)),
                ('money_warning_threshold', models.FloatField(default=15)),
                ('transaction_cancel_threshold', models.FloatField(default=48)),
                ('agios_enabled', models.BooleanField(default=True)),
                ('agios_threshold', models.FloatField(default=2)),
                ('agios_factor', models.FloatField(default=0.05)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RunPython(migrate_barsettings),
        migrations.RemoveField(
            model_name='bar',
            name='agios_enabled',
        ),
        migrations.RemoveField(
            model_name='bar',
            name='agios_factor',
        ),
        migrations.RemoveField(
            model_name='bar',
            name='agios_threshold',
        ),
        migrations.RemoveField(
            model_name='bar',
            name='last_modified',
        ),
        migrations.RemoveField(
            model_name='bar',
            name='money_warning_threshold',
        ),
        migrations.RemoveField(
            model_name='bar',
            name='next_scheduled_appro',
        ),
        migrations.RemoveField(
            model_name='bar',
            name='transaction_cancel_threshold',
        ),
    ]
