# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    def migrate_moneyflow(apps, schema_editor):
        Transaction = apps.get_model("bars_transactions", "Transaction")
        for tsc in Transaction.objects.all():
            t = tsc.type
            iops = tsc.itemoperation_set.all()
            aops = tsc.accountoperation_set.all()
            data = tsc.transactiondata_set.all()
            m = 0

            if t in ["buy", "withdraw", "agios", "barInvestment", "appro"]:
                m = -aops[0].delta

            if t == "throw":
                si = iops[0].target
                si_price = si.price * (1. + si.sellitem.tax)
                m = iops[0].delta * si_price

            if t in ["deposit", "punish"]:
                m = aops[0].delta

            if t == "give":
                from_op = aops[0]
                to_op = aops[1]
                if to_op.target.owner == transaction.author:
                    from_op, to_op = to_op, from_op
                m = to_op.delta

            if t == "refund":
                for aop in aops:
                    if aop.target.owner != get_default_user():
                        return aop.delta

            if t in ["meal", "collectivePayment"]:
                for aop in aops:
                    m += abs(aop.delta)

            if t == "inventory":
                for iop in iops:
                    si = iop.target
                    si_price = si.price * (1. + si.sellitem.tax)
                    m += iop.delta * si_price

            tsc.moneyflow = m
            tsc.save()

    def reverse_moneyflow(apps, schema_editor):
        Transaction = apps.get_model("bars_transactions", "Transaction")
        for t in Transaction.objects.all():
            t.moneyflow = 0.0
            t.save()

    dependencies = [
        ('bars_transactions', '0002_manual'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='moneyflow',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.RunPython(
            migrate_moneyflow,
            reverse_moneyflow
        )
    ]
