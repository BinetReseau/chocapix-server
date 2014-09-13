from django.db import models
from rest_framework import viewsets, routers, mixins, status
from rest_framework import serializers
from django.core.exceptions import ValidationError

from rest_framework import fields
class VirtualField(fields.Field):
    type_name = 'VirtualField'
    type_label = 'virtual'
    label = 'virtual'

    def __init__(self, value):
        self.value = value

    # def validate(self, value):
    #     pass

    def field_to_native(self, obj, field_name):
        return self.value

    def field_from_native(self, data, files, field_name, into):
        pass

    # def from_native(self, value):
    #     return value


## User
class User(models.Model):
    login = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)

    name = models.CharField(max_length=100)
    pseudo = models.CharField(max_length=50)

    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('login', 'name', 'pseudo', 'last_modified')
        write_only_fields = ('password',)
    _type = VirtualField("User")

## Bar
class Bar(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.id

class BarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bar
    _type = VirtualField("Bar")

## Account
class Account(models.Model):
    class Meta:
        unique_together = (("bar", "owner"))
    bar = models.ForeignKey(Bar)
    owner = models.ForeignKey(User)
    money = models.DecimalField(max_digits=7, decimal_places=3)
    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.owner.name + " ("+self.bar.id+")"

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
    _type = VirtualField("Account")

## Item
class Item(models.Model):
    bar = models.ForeignKey(Bar)
    name = models.CharField(max_length=100)
    qty = models.DecimalField(max_digits=7, decimal_places=3)
    price = models.DecimalField(max_digits=7, decimal_places=3)
    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
    _type = VirtualField("Item")

## Transaction
class Transaction(models.Model):
    bar = models.ForeignKey(Bar)
    author = models.ForeignKey(User)
    type = models.CharField(max_length=25)
    timestamp = models.DateTimeField(auto_now_add=True)
    canceled = models.BooleanField()
    last_modified = models.DateTimeField(auto_now=True)
class AccountOperation(models.Model):
    transaction = models.ForeignKey(Transaction)
    account = models.ForeignKey(Account)
    delta = models.DecimalField(max_digits=7, decimal_places=3)

class ItemOperation(models.Model):
    transaction = models.ForeignKey(Transaction)
    item = models.ForeignKey(Item)
    delta = models.DecimalField(max_digits=7, decimal_places=3)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction


class BuyTransactionSerializer(TransactionSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    qty = serializers.DecimalField(max_digits=7, decimal_places=3)

    def save_object(self, t, **kwargs):
        super(BuyTransactionSerializer, self).save_object(t, **kwargs)

        t.itemoperation_set.create(
            item=t.item,
            delta=t.qty)
        t.accountoperation_set.create(
            account=Account.objects.get(owner=t.author, bar=t.bar),
            delta=t.qty*t.item.price)

    def to_native(self, transaction):
        obj = super(BuyTransactionSerializer, self).to_native(transaction)
        if transaction is None: return obj

        try:
            error = serializers.ValidationError("")

            if len(transaction.itemoperation_set.all()) != 1:
                raise error
            iop = transaction.itemoperation_set.all()[0]
            obj["item"] = iop.item.id
            obj["qty"] = abs(iop.delta)

            if len(transaction.accountoperation_set.all()) != 1:
                raise error
            if transaction.accountoperation_set.all()[0].account.owner != transaction.author:
                raise error

        except serializers.ValidationError:
            obj["_type"] = "Transaction"
            # return obj
        else:
            obj["_type"] = transaction.type.title() + "Transaction"

        return obj



class GiveTransactionSerializer(TransactionSerializer):
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
        if transaction is None: return obj

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
            if from_op.delta <= 0 and from_op.delta != -to_op.delta:
                raise error
            obj["account"] = to_op.account.id

        except serializers.ValidationError:
            obj["_type"] = "Transaction"
            # return obj
        else:
            obj["_type"] = transaction.type.title() + "Transaction"

        return obj


class TransactionViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                           mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Transaction.objects.all()
    serializer_class = BuyTransactionSerializer
