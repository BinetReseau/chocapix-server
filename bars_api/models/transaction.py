from django.db import models
from django.db.models import F, Q
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
    prev_value = models.FloatField()
    delta = models.FloatField()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.prev_value = self.item.qty
            Item.objects.filter(pk=self.item.id).update(qty=F('qty') + self.delta)
        super(ItemOperation, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.item) + "+=" + unicode(self.delta)

    def repropagate(self):
        olders = (ItemOperation.objects.select_related()
                  .filter(item=self.item)
                  .filter(transaction__timestamp__gte=self.transaction.timestamp)
                  .order_by('transaction__timestamp'))
        next_prev = self.prev_value
        for iop in olders:
            iop.prev_value = next_prev
            if not iop.transaction.canceled:
                next_prev += iop.delta
            iop.save()
        Item.objects.filter(pk=self.item.id).update(qty=next_prev)



class AccountOperation(models.Model):
    class Meta:
        app_label = 'bars_api'
    transaction = models.ForeignKey(Transaction)
    account = models.ForeignKey(Account)
    prev_value = models.FloatField()
    delta = models.FloatField()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.prev_value = self.account.money
            Account.objects.filter(pk=self.account.id).update(money=F('money') + self.delta)
        super(AccountOperation, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.account) + "+=" + unicode(self.delta)

    def repropagate(self):
        olders = (AccountOperation.objects.select_related()
                  .filter(account=self.account)
                  .filter(transaction__timestamp__gte=self.transaction.timestamp)
                  .order_by('transaction__timestamp'))
        next_prev = self.prev_value
        for aop in olders:
            aop.prev_value = next_prev
            if not aop.transaction.canceled:
                next_prev += aop.delta
            aop.save()
        Account.objects.filter(pk=self.account.id).update(money=next_prev)



# ######################### Transaction Serializers ########################## #

class BaseTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        read_only_fields = ('bar', 'author', 'timestamp', 'last_modified')

    def to_representation(self, transaction):
        if 'ignore_type' in self.context or transaction.type == "":
            obj = super(BaseTransactionSerializer, self).to_representation(transaction)
            try:
                author_account = Account.objects.get(owner=transaction.author, bar=transaction.bar)
                obj["author_account"] = author_account.id
            except:
                pass
            obj['_type'] = "Transaction"

            return obj
        else:
            serializer = serializers_class_map[transaction.type](transaction)
            return serializer.data

    def create(self, data):
        fields = Transaction._meta.get_all_field_names()
        attrs = {k: v for k, v in data.items() if k in fields}
        t = Transaction(**attrs)
        t.author = self.context['request'].user
        # Todo: add correct bar
        t.bar = Bar.objects.all()[0]  # self.context['request'].bar
        t.save()
        return t


class BuyTransactionSerializer(BaseTransactionSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    qty = serializers.FloatField()

    def create(self, data):
        t = super(BuyTransactionSerializer, self).create(data)

        t.itemoperation_set.create(
            item=data['item'],
            delta=-data['qty'])
        t.accountoperation_set.create(
            account=Account.objects.get(owner=t.author, bar=t.bar),
            delta=-data['qty'] * data['item'].price)

        return t

    def to_representation(self, transaction):
        obj = BaseTransactionSerializer(transaction, context={'ignore_type': True}).data
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


class ThrowTransactionSerializer(BaseTransactionSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    qty = serializers.FloatField()

    def create(self, data):
        t = super(ThrowTransactionSerializer, self).create(data)

        t.itemoperation_set.create(
            item=data["item"],
            delta=-data["qty"])

        return t

    def to_representation(self, transaction):
        obj = BaseTransactionSerializer(transaction, context={'ignore_type': True}).data
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


class MealItemSerializer(serializers.Serializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    qty = serializers.FloatField()

class MealAccountSerializer(serializers.Serializer):
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    ratio = serializers.FloatField()

class MealTransactionSerializer(BaseTransactionSerializer):
    items = MealItemSerializer(many=True)
    accounts = MealAccountSerializer(many=True)

    def create(self, data):
        t = super(MealTransactionSerializer, self).create(data)

        total_price = 0
        for i in data["items"]:
            t.itemoperation_set.create(
                item=i["item"],
                delta=-i["qty"])
            total_price += i["qty"] * i["item"].price

        total_ratio = 0
        for a in data["accounts"]:
            total_ratio += a["ratio"]
        for a in data["accounts"]:
            t.accountoperation_set.create(
                account=a["account"],
                delta=-total_price * a["ratio"] / total_ratio)

        return t

    def to_representation(self, transaction):
        obj = BaseTransactionSerializer(transaction, context={'ignore_type': True}).data
        if transaction is None:
            return obj

        obj["items"] = []
        for iop in transaction.itemoperation_set.all():
            obj["items"].append({
                'item': iop.item.id,
                'qty': abs(iop.delta)
            })

        total_price = 0
        obj["accounts"] = []
        aops = transaction.accountoperation_set.all()
        for aop in aops:
            total_price += abs(aop.delta)
        for aop in aops:
            obj["accounts"].append({
                'account': aop.account.id,
                'ratio': abs(aop.delta) / total_price
            })

        obj["moneyflow"] = total_price

        return obj


class GiveTransactionSerializer(BaseTransactionSerializer):
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    amount = serializers.FloatField()

    def create(self, data):
        t = super(GiveTransactionSerializer, self).create(data)

        t.accountoperation_set.create(
            account=Account.objects.get(owner=t.author, bar=t.bar),
            delta=-data["amount"])
        t.accountoperation_set.create(
            account=data["account"],
            delta=data["amount"])

        return t

    def to_representation(self, transaction):
        obj = BaseTransactionSerializer(transaction, context={'ignore_type': True}).data
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


class PunishTransactionSerializer(BaseTransactionSerializer):
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    amount = serializers.FloatField()
    motive = serializers.CharField()

    def create(self, data):
        t = super(PunishTransactionSerializer, self).create(data)

        t.accountoperation_set.create(
            account=data["account"],
            delta=-data["amount"])
        t.transactiondata_set.create(
            label='motive',
            data=data["motive"])

        return t

    def to_representation(self, transaction):
        obj = BaseTransactionSerializer(transaction, context={'ignore_type': True}).data
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


serializers_class_map = {
    "": BaseTransactionSerializer,
    "buy": BuyTransactionSerializer,
    "meal": MealTransactionSerializer,
    "give": GiveTransactionSerializer,
    "throw": ThrowTransactionSerializer,
    "punish": PunishTransactionSerializer}

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()

    def get_serializer_class(self):
        data = self.request.data
        if "type" in data:
            return serializers_class_map[data["type"]]
        else:
            return serializers_class_map[""]

    def get_queryset(self):
        queryset = Transaction.objects.all()

        user = self.request.QUERY_PARAMS.get('user', None)
        if user is not None:
            queryset = queryset.filter(
                Q(accountoperation__account__owner=user) |
                Q(author=user)
            )

        account = self.request.QUERY_PARAMS.get('account', None)
        if account is not None:
            queryset = queryset.filter(
                Q(accountoperation__account=account) |
                Q(author__account=account)
            )

        item = self.request.QUERY_PARAMS.get('item', None)
        if item is not None:
            queryset = queryset.filter(itemoperation__item=item)

        queryset = queryset.order_by('-timestamp')
        # queryset = queryset.order_by('-timestamp').distinct('timestamp')

        page = int(self.request.QUERY_PARAMS.get('page', 0))
        if page != 0:
            page_size = int(self.request.QUERY_PARAMS.get('page_size', 10))
            queryset = queryset[(page - 1) * page_size: page * page_size]

        return queryset


    @decorators.detail_route(methods=['post'])
    def cancel(self, request, pk=None):
        transaction = Transaction.objects.select_related().get(pk=pk)
        transaction.canceled = True
        transaction.save()

        for aop in transaction.accountoperation_set.all():
            aop.repropagate()

        for iop in transaction.itemoperation_set.all():
            iop.repropagate()

        serializer = self.get_serializer_class()(transaction)
        return Response(serializer.data)

    @decorators.detail_route(methods=['post'])
    def restore(self, request, pk=None):
        transaction = Transaction.objects.get(pk=pk)
        transaction.canceled = False
        transaction.save()

        for aop in transaction.accountoperation_set.all():
            aop.repropagate()

        for iop in transaction.itemoperation_set.all():
            iop.repropagate()

        serializer = self.get_serializer_class()(transaction)
        return Response(serializer.data)
