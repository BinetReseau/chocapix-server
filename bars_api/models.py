from django.db import models
from rest_framework import viewsets, routers, mixins, status
from rest_framework import serializers, decorators
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from rest_framework import fields
class VirtualField(fields.Field):
    type_name = 'VirtualField'
    type_label = 'virtual'
    label = 'virtual'
    source = ''

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
        fields = ('id', '_type', 'login', 'name', 'pseudo', 'last_modified')
        write_only_fields = ('password',)
    _type = VirtualField("User")

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @decorators.list_route()
    def me(self, request):
        serializer = self.serializer_class(self.queryset[0]) # Todo: request.user
        return Response(serializer.data)

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

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    @decorators.list_route(methods=['get'])
    def me(self, request):
        serializer = self.serializer_class(self.queryset[0])
        return Response(serializer.data)

## Item
class Item(models.Model):
    bar = models.ForeignKey(Bar)
    name = models.CharField(max_length=100)
    keywords = models.CharField(max_length=200) # Todo: length
    qty = models.DecimalField(max_digits=7, decimal_places=3)
    price = models.DecimalField(max_digits=7, decimal_places=3)
    deleted = models.BooleanField(default = False)
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
    canceled = models.BooleanField(default = False)
    last_modified = models.DateTimeField(auto_now=True)

    # def clean(self):
    #     error = ValidationError("Invalid '%s' transaction (id=%s)"%(self.type, self.id))
    #     try:
    #         if self.type in ["buy", "throw"]:
    #             if len(self.itemoperation_set.all()) != 1:
    #                 raise error

    #         if self.type in ["throw"]:
    #             if len(self.accountoperation_set.all()) != 0:
    #                 raise error

    #         if self.type in ["buy"]:
    #             if len(self.accountoperation_set.all()) != 1:
    #                 raise error
    #             if self.accountoperation_set.all()[0].account.owner != self.author:
    #                 raise error

    #         if self.type in ["give"]:
    #             if len(self.accountoperation_set.all()) != 2:
    #                 raise error
    #             from_account = self.accountoperation_set.all()[0]
    #             to_account = self.accountoperation_set.all()[1]
    #             if from_account.delta > 0:
    #                 from_account, to_account = to_account, from_account
    #             if from_account.delta != -to_account.delta:
    #                 raise error
    #             if from_account.owner != self.author:
    #                 raise error

    #         if self.type in ["appro", "inventory"]:
    #             pass
    #     except ValidationError:
    #         self.type=""


class AccountOperation(models.Model):
    transaction = models.ForeignKey(Transaction)
    account = models.ForeignKey(Account)
    delta = models.DecimalField(max_digits=7, decimal_places=3)

class ItemOperation(models.Model):
    transaction = models.ForeignKey(Transaction)
    item = models.ForeignKey(Item)
    delta = models.DecimalField(max_digits=7, decimal_places=3)



class BaseTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        read_only_fields = ('bar', 'author', 'timestamp', 'last_modified')

    def to_native(self, transaction):
        fields = self.fields
        self.fields = {k:v for k,v in self.fields.items() if k in ('id', 'bar', 'author', 'type', 'timestamp', 'last_modified', 'canceled')}
        obj = super(BaseTransactionSerializer, self).to_native(transaction)
        self.fields = fields
        return obj


    def restore_object(self, attrs, instance=None):
        t = super(BaseTransactionSerializer, self).restore_object(attrs, instance)
        # Todo: add correct author/bar
        t.author = User.objects.all()[0] # self.context['request'].user
        t.bar = Bar.objects.all()[0] # self.context['request'].bar
        return t

    # def to_native(self, transaction):
    #     if transaction is None:
    #         return super(TransactionSerializer, self).to_native(transaction)

    #     # try:
    #     #     transaction.clean()
    #     # except ValidationError as e:
    #     #     raise serializers.ValidationError(e.message_dict)
    #     obj = super(TransactionSerializer, self).to_native(transaction)

    #     try:
    #         if transaction.type in ["buy", "throw"]:
    #             if len(transaction.itemoperation_set.all()) != 1:
    #                 raise serializers.ValidationError("")
    #             iop = transaction.itemoperation_set.all()[0]
    #             obj["item"] = iop.item.id
    #             obj["qty"] = abs(iop.delta)

    #         if transaction.type in ["throw"]:
    #             if len(transaction.accountoperation_set.all()) != 0:
    #                 raise serializers.ValidationError("")

    #         if transaction.type in ["buy"]:
    #             if len(transaction.accountoperation_set.all()) != 1:
    #                 raise serializers.ValidationError("")
    #             if transaction.accountoperation_set.all()[0].account.owner != transaction.author:
    #                 raise serializers.ValidationError("")

    #         if transaction.type in ["give"]:
    #             if len(transaction.accountoperation_set.all()) != 2:
    #                 raise serializers.ValidationError("")
    #             from_account = transaction.accountoperation_set.all()[0]
    #             to_account = transaction.accountoperation_set.all()[1]
    #             if from_account.delta > 0:
    #                 from_account, to_account = to_account, from_account
    #             if from_account.delta != -to_account.delta:
    #                 raise serializers.ValidationError("")
    #             if from_account.owner != transaction.author:
    #                 raise serializers.ValidationError("")
    #             obj["to_account"] = to_account.id

    #         if transaction.type in ["appro", "inventory"]:
    #             pass

    #     except serializers.ValidationError:
    #         obj["type"] = ""
    #         return obj

    #     obj["type"] = transaction.type.title() + "Transaction"

    #     return obj

    # def validate(self, attrs):
    #     if not super(serializers.ModelSerializer, self).validate(attrs):
    #         return False



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
            delta=-t.qty*t.item.price)

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
            aop = transaction.accountoperation_set.all()[0]
            if aop.account.owner != transaction.author:
                raise error
            obj["moneyflow"] = -aop.delta

        except serializers.ValidationError:
            obj["_type"] = "Transaction"
            # return obj
        else:
            # obj["_type"] = transaction.type.title() + "Transaction"
            obj["_type"] = "Transaction"

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
            if from_op.delta >= 0 or from_op.delta != -to_op.delta:
                raise error
            obj["account"] = to_op.account.id
            obj["amount"] = to_op.delta
            obj["moneyflow"] = to_op.delta

        except serializers.ValidationError:
            obj["_type"] = "Transaction"
            # return obj
        else:
            # obj["_type"] = transaction.type.title() + "Transaction"
            obj["_type"] = "Transaction"

        return obj



class TransactionSerializer(serializers.Serializer):
    serializers_class_map = {
        "": BaseTransactionSerializer,
        "buy": BuyTransactionSerializer,
        "give": GiveTransactionSerializer}

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
        transaction.canceled = True;
        transaction.save()
        serializer = self.serializer_class(transaction)
        return Response(serializer.data)

    @decorators.detail_route(methods=['post'])
    def restore(self, request, pk=None):
        transaction = Transaction.objects.get(pk=pk)
        transaction.canceled = False;
        transaction.save()
        serializer = self.serializer_class(transaction)
        return Response(serializer.data)
