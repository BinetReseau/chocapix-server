# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    def migrate_moneyflow(apps, schema_editor):
        Transaction = apps.get_model("bars_transactions", "Transaction")
        User = apps.get_model("bars_core", "User")
        for tsc in Transaction.objects.all():
            t = tsc.type
            iops = tsc.itemoperation_set.all()
            aops = tsc.accountoperation_set.all()
            data = tsc.transactiondata_set.all()
            m = 0

            try:
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
                    if to_op.target.owner == tsc.author:
                        from_op, to_op = to_op, from_op
                    m = to_op.delta

                if t == "refund":
                    default_user = User.objects.get_or_create(username="bar", firstname="Bar", is_active=False)
                    for aop in aops:
                        if aop.target.owner != default_user:
                            m += aop.delta

                if t in ["meal", "collectivePayment"]:
                    for aop in aops:
                        m += abs(aop.delta)

                if t == "inventory":
                    for iop in iops:
                        si = iop.target
                        si_price = si.price * (1. + si.sellitem.tax)
                        m += iop.delta * si_price
            except Exception as inst:
                print(type(inst))
                print(inst.args)
                print(inst)

            tsc.moneyflow = m
            tsc.save()

    def reverse_moneyflow(apps, schema_editor):
        Transaction = apps.get_model("bars_transactions", "Transaction")
        for t in Transaction.objects.all():
            t.moneyflow = 0.0
            t.save()

    dependencies = [
        ('bars_transactions', '0002_manual'),
        ('bars_core', '0017_auto_20150726_1506')
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
