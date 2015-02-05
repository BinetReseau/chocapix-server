from django.db import models

from bars_core.models.user import User
from bars_django.utils import VirtualField
from bars_core.models.bar import Bar
from bars_base.models.item import Item
from bars_base.models.account import Account


class Transaction(models.Model):
    class Meta:
        app_label = 'bars_transactions'
    bar = models.ForeignKey(Bar)
    author = models.ForeignKey(User)
    type = models.CharField(max_length=25)
    timestamp = models.DateTimeField(auto_now_add=True)
    canceled = models.BooleanField(default=False)
    last_modified = models.DateTimeField(auto_now=True)
    _type = VirtualField("Transaction")

    def __unicode__(self):
        return self.type + ": " \
            + unicode(list(self.accountoperation_set.all())
                      + list(self.itemoperation_set.all())
                      + list(self.transactiondata_set.all()))

    def check_integrity(self):
        t = self.type
        iops = self.itemoperation_set.all()
        aops = self.accountoperation_set.all()
        data = self.transactiondata_set.all()

        if t in ["buy", "throw"] and len(iops) != 1:
            return False

        if t in ["throw"] and len(aops) != 0:
            return False
        if t in ["buy", "throw", "appro", "inventory"] and len(aops) != 1:
            return False
        if t in ["give", "punish"] and len(aops) != 2:
            return False

        if t in ["meal", "punish"] and len(data) != 1:
            return False

        # TODO: Check money flow, owners, signs, labels, ...
        return True



class TransactionData(models.Model):
    class Meta:
        app_label = 'bars_transactions'
    transaction = models.ForeignKey(Transaction)
    label = models.CharField(max_length=128)
    data = models.TextField()


class BaseOperation(models.Model):
    class Meta:
        abstract = True
    transaction = models.ForeignKey(Transaction)
    prev_value = models.FloatField()
    fixed = models.BooleanField(default=False)  # Whether the operation was a delta or a fixed value
    delta = models.FloatField()  # Fixed if not self.fixed
    next_value = models.FloatField()  # Fixed if self.fixed

    def __unicode__(self):
        if self.fixed:
            return unicode(self.target) + "=" + unicode(self.next_value)
        else:
            return unicode(self.target) + "+=" + unicode(self.delta)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.prev_value = getattr(self.target, self.op_model_field)

        if self.fixed:
            self.delta = self.next_value - self.prev_value
        else:
            self.next_value = self.prev_value + self.delta

        if not self.pk:
            self.op_model.objects.filter(pk=self.target.id).update(**{self.op_model_field: self.next_value})

        super(BaseOperation, self).save(*args, **kwargs)

    def propagate(self):
        olders_or_self = (self.__class__.objects.select_related()
                          .filter(target=self.target)
                          .filter(transaction__timestamp__gte=self.transaction.timestamp)
                          .order_by('transaction__timestamp', 'pk'))

        next_prev = None
        for op in olders_or_self:
            if next_prev is not None:
                op.prev_value = next_prev
                op.save()

            if op.transaction.canceled:
                next_prev = op.prev_value
            else:
                next_prev = op.next_value

        self.op_model.objects.filter(pk=self.target.id).update(**{self.op_model_field: next_prev})

class ItemOperation(BaseOperation):
    class Meta:
        app_label = 'bars_transactions'
    target = models.ForeignKey(Item)

    op_model = Item
    op_model_field = 'qty'

class AccountOperation(BaseOperation):
    class Meta:
        app_label = 'bars_transactions'
    target = models.ForeignKey(Account)

    op_model = Account
    op_model_field = 'money'
