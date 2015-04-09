# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def correct_refundtransactions(apps, schema_editor):
    User = apps.get_model("bars_core", "User")
    Account = apps.get_model("bars_core", "Account")
    Transaction = apps.get_model("bars_transactions", "Transaction")
    AccountOperation = apps.get_model("bars_transactions", "AccountOperation")
    default_user, _ = User.objects.get_or_create(username="bar", firstname="Bar", is_active=False)

    for t in Transaction.objects.filter(type="refund"):
        if t.accountoperation_set.all().count() == 1:
            default_account, _ = Account.objects.get_or_create(owner=default_user, bar=t.bar)
            op = t.accountoperation_set.all()[0]

            nop = AccountOperation(
                transaction=t,
                target=default_account,
                delta=abs(op.delta))
            nop.prev_value = default_account.money
            nop.next_value = nop.prev_value + nop.delta
            nop.save()


class Migration(migrations.Migration):

    dependencies = [
        ('bars_transactions', '0001_initial'),
        ('bars_core', '0015_auto_20150329_1856'),
    ]

    operations = [
        migrations.RunPython(correct_refundtransactions),
    ]
