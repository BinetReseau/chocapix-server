from django.db import models
from rest_framework import viewsets
from rest_framework import serializers, decorators
from rest_framework.response import Response

from bars_api.auth import User
from bars_api.models import VirtualField
from bars_api.models.bar import Bar
from bars_api.models.item import Item
from bars_api.models.account import Account


class Transaction(models.Model):
    class Meta:
        app_label = 'bars_api'
    bar = models.ForeignKey(Bar)
    author = models.ForeignKey(User)
    type = models.CharField(max_length=25)
    timestamp = models.DateTimeField(auto_now_add=True)
    canceled = models.BooleanField(default=False)
    last_modified = models.DateTimeField(auto_now=True)
    _type = VirtualField("Transaction")


class TransactionData(models.Model):
    class Meta:
        app_label = 'bars_api'
    transaction = models.ForeignKey(Transaction)
    label = models.CharField(max_length=128)
    data = models.TextField()


class ItemOperation(models.Model):
    class Meta:
        app_label = 'bars_api'
    transaction = models.ForeignKey(Transaction)
    item = models.ForeignKey(Item)
    prev_value = models.DecimalField(max_digits=7, decimal_places=3)
    delta = models.DecimalField(max_digits=7, decimal_places=3)

    def save(self, *args, **kwargs):
        isNew = not self.pk
        if isNew:
            self.prev_value = self.item.qty
        super(ItemOperation, self).save(*args, **kwargs)
        if isNew:
            self.item.qty = self.prev_value + self.delta
            self.item.save()


class AccountOperation(models.Model):
    class Meta:
        app_label = 'bars_api'
    transaction = models.ForeignKey(Transaction)
    account = models.ForeignKey(Account)
    prev_value = models.DecimalField(max_digits=7, decimal_places=3)
    delta = models.DecimalField(max_digits=7, decimal_places=3)

    def save(self, *args, **kwargs):
        isNew = not self.pk
        if isNew:
            self.prev_value = self.account.money
        super(AccountOperation, self).save(*args, **kwargs)
        if isNew:
            self.account.money = self.prev_value + self.delta
            self.account.save()



class BaseTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        read_only_fields = ('bar', 'author', 'timestamp', 'last_modified')

    def to_native(self, t):
        fields = self.fields
        self.fields = {k: v for k, v in self.fields.items() if k in
                ('id', 'bar', 'author', 'type', 'timestamp',
                 'last_modified', 'canceled', '_type')}
        obj = super(BaseTransactionSerializer, self).to_native(t)
        self.fields = fields
        try:
            author_account = Account.objects.get(owner=t.author, bar=t.bar)
            obj["author_account"] = author_account.id
        except:
            pass
        obj['_type'] = "Transaction"
        return obj

    def restore_object(self, attrs, instance=None):
        t = super(BaseTransactionSerializer, self).restore_object(attrs, instance)
        t.author = self.context['request'].user
        # Todo: add correct bar
        t.bar = Bar.objects.all()[0]  # self.context['request'].bar
        return t


class BuyTransactionSerializer(BaseTransactionSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    qty = serializers.DecimalField(max_digits=7, decimal_places=3)

    def save_object(self, t, **kwargs):
        super(BuyTransactionSerializer, self).save_object(t, **kwargs)

        t.itemoperation_set.create(
            item=t.item,
            delta=-t.qty)
        t.accountoperation_set.create(
            account=Account.objects.get(owner=t.author, bar=t.bar),
            delta=-t.qty * t.item.price)

    def to_native(self, transaction):
        obj = super(BuyTransactionSerializer, self).to_native(transaction)
        if transaction is None:
            return obj

        try:
            error = serializers.ValidationError("")

            if len(transaction.itemoperation_set.all()) != 1:
                raise error
            iop = transaction.itemoperation_set.all()[0]
            obj["item"] = iop.item.id
            obj["qty"] = abs(iop.delta)

            if len(transaction.accountoperation_set.all()) != 1:
                raise error
            aop = transaction.accountoperation_set.all()[0]
            if aop.account.owner != transaction.author:
                raise error
            obj["moneyflow"] = -aop.delta

        except serializers.ValidationError:
            return obj
        else:
            pass
            # obj["_type"] = transaction.type.title() + "Transaction"

        return obj


class GiveTransactionSerializer(BaseTransactionSerializer):
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    amount = serializers.DecimalField(max_digits=7, decimal_places=3)

    def save_object(self, t, **kwargs):
        super(GiveTransactionSerializer, self).save_object(t, **kwargs)

        t.accountoperation_set.create(
            account=Account.objects.get(owner=t.author, bar=t.bar),
            delta=-t.amount)
        t.accountoperation_set.create(
            account=t.account,
            delta=t.amount)

    def to_native(self, transaction):
        obj = super(GiveTransactionSerializer, self).to_native(transaction)
        if transaction is None:
            return obj

        try:
            error = serializers.ValidationError("")

            if len(transaction.accountoperation_set.all()) != 2:
                raise error
            from_op = transaction.accountoperation_set.all()[0]
            to_op = transaction.accountoperation_set.all()[1]
            if from_op.account.owner != transaction.author:
                from_op, to_op = to_op, from_op
            if from_op.account.owner != transaction.author:
                raise error
            if from_op.delta >= 0 or from_op.delta != -to_op.delta:
                raise error
            obj["account"] = to_op.account.id
            obj["amount"] = to_op.delta
            obj["moneyflow"] = to_op.delta

        except serializers.ValidationError:
            return obj
        else:
            pass
            # obj["_type"] = transaction.type.title() + "Transaction"

        return obj


class ThrowTransactionSerializer(BaseTransactionSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    qty = serializers.DecimalField(max_digits=7, decimal_places=3)

    def save_object(self, t, **kwargs):
        super(ThrowTransactionSerializer, self).save_object(t, **kwargs)

        # t.accountoperation_set.create(
        #     account=Account.objects.get(owner=t.author, bar=t.bar),
        #     delta=-t.amount)
        t.itemoperation_set.create(
            item=t.item,
            delta=-t.qty)

    def to_native(self, transaction):
        obj = super(ThrowTransactionSerializer, self).to_native(transaction)
        if transaction is None:
            return obj

        try:
            error = serializers.ValidationError("")

            if len(transaction.itemoperation_set.all()) != 1:
                raise error
            iop = transaction.itemoperation_set.all()[0]
            obj["item"] = iop.item.id
            obj["qty"] = abs(iop.delta)

            # if len(transaction.accountoperation_set.all()) != 1:
            #     raise error
            # aop = transaction.accountoperation_set.all()[0]
            # if aop.account != # bar.account:
            #     raise error
            # obj["moneyflow"] = -aop.delta
            # obj["account"] = aop.account.id
            obj["moneyflow"] = iop.delta * iop.item.price


        except serializers.ValidationError:
            return obj
        else:
            pass
            # obj["_type"] = transaction.type.title() + "Transaction"

        return obj


class PunishTransactionSerializer(BaseTransactionSerializer):
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    amount = serializers.DecimalField(max_digits=7, decimal_places=3)
    motive = serializers.CharField()

    def save_object(self, t, **kwargs):
        super(PunishTransactionSerializer, self).save_object(t, **kwargs)

        t.accountoperation_set.create(
            account=t.account,
            delta=-t.amount)
        t.transactiondata_set.create(
            label='motive',
            data=t.motive)

    def to_native(self, transaction):
        obj = super(PunishTransactionSerializer, self).to_native(transaction)
        if transaction is None:
            return obj

        try:
            error = serializers.ValidationError("")

            if len(transaction.accountoperation_set.all()) != 1:
                raise error
            aop = transaction.accountoperation_set.all()[0]
            obj["account"] = aop.account.id
            obj["amount"] = aop.delta

            if len(transaction.transactiondata_set.all()) != 1:
                raise error
            data = transaction.transactiondata_set.all()[0]
            if data.label != 'motive':
                raise error
            obj["motive"] = data.data
            obj["moneyflow"] = aop.delta


        except serializers.ValidationError:
            return obj
        else:
            pass
            # obj["_type"] = transaction.type.title() + "Transaction"

        return obj


class TransactionSerializer(serializers.Serializer):
    serializers_class_map = {
        "": BaseTransactionSerializer,
        "buy": BuyTransactionSerializer,
        "give": GiveTransactionSerializer,
        "throw": ThrowTransactionSerializer,
        "punish": PunishTransactionSerializer}

    def __init__(self, *args, **kwargs):
        super(TransactionSerializer, self).__init__(*args, **kwargs)
        self.serializers_map = {}
        for key, serializer in self.serializers_class_map.items():
            self.serializers_map[key] = serializer(*args, **kwargs)

    def get_serializer(self, obj):
        if obj is None:
            type = ""
        elif isinstance(obj, dict):
            type = obj.get("type", "")
        else:
            type = obj.type or ""

        if type in self.serializers_map:
            return self.serializers_map[type]
        else:
            return self.serializers_map[""]

    def to_native(self, obj):
        return self.get_serializer(obj).to_native(obj)

    def from_native(self, data, files=None):
        s = self.get_serializer(data)
        s._errors = self._errors
        ret = self.get_serializer(data).from_native(data, files)
        self._errors = s._errors
        return ret

    def restore_fields(self, data, files):
        s = self.get_serializer(data)
        s._errors = self._errors
        ret = s.restore_fields(data, files)
        self._errors = s._errors
        return ret

    def save_object(self, obj, **kwargs):
        self.get_serializer(obj).save_object(obj, **kwargs)


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @decorators.detail_route(methods=['post'])
    def cancel(self, request, pk=None):
        transaction = Transaction.objects.get(pk=pk)
        transaction.canceled = True
        transaction.save()
        serializer = self.serializer_class(transaction)
        return Response(serializer.data)

    @decorators.detail_route(methods=['post'])
    def restore(self, request, pk=None):
        transaction = Transaction.objects.get(pk=pk)
        transaction.canceled = False
        transaction.save()
        serializer = self.serializer_class(transaction)
        return Response(serializer.data)
