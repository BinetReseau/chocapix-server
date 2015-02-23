from django.http import Http404
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework import exceptions

from bars_base.models.item import Item
from bars_base.models.account import Account, get_default_account
from bars_transactions.models import Transaction


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
            # serializer.is_valid(raise_exception=True)
            try:
                return serializer.data
            except:
                return

    def create(self, data):
        request = self.context['request']
        bar = request.bar
        if bar is None:
            raise Http404()

        if request.user.has_perm('bars_transactions.add_' + data["type"] + 'transaction', bar):
            fields = Transaction._meta.get_all_field_names()
            attrs = {k: v for k, v in data.items() if k in fields}
            t = Transaction(**attrs)
            # t.author = User.objects.all()[0]
            t.author = request.user
            t.bar = bar
            t.save()
            return t

        else:
            raise exceptions.PermissionDenied()



class ItemQtySerializer(serializers.Serializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    qty = serializers.FloatField()

    def validate_qty(self, value):
        if value < 0:
            raise ValidationError("Quantity must be positive")
        return value

    def validate_item(self, item):
        if item.deleted:
            raise ValidationError("Item is deleted")
        return item


class ItemQtyPriceSerializer(ItemQtySerializer):
    price = serializers.FloatField(required=False)

    def validate_price(self, value):
        if value is not None and value < 0:
            raise ValidationError("Price must be positive")
        return value


class AccountAmountSerializer(serializers.Serializer):
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    amount = serializers.FloatField()

    def validate_account(self, account):
        if account.deleted:
            raise ValidationError("Account is deleted")
        return account

    def validate_amount(self, value):
        if value < 0:
            raise ValidationError("Amount must be positive")
        return value


class AccountRatioSerializer(serializers.Serializer):
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    ratio = serializers.FloatField()

    def validate_account(self, account):
        if account.deleted:
            raise ValidationError("Account is deleted")
        return account

    def validate_ratio(self, value):
        if value <= 0:
            raise ValidationError("Ratio must be positive")
        return value



class BuyTransactionSerializer(BaseTransactionSerializer, ItemQtySerializer):
    def validate_item(self, item):
        item = super(BuyTransactionSerializer, self).validate_item(item)

        if self.context['request'].bar.id != item.bar.id:
            raise serializers.ValidationError("Cannot buy across bars")

        return item

    def create(self, data):
        t = super(BuyTransactionSerializer, self).create(data)

        t.itemoperation_set.create(
            target=data['item'],
            delta=-data['qty'])
        t.accountoperation_set.create(
            target=Account.objects.get(owner=t.author, bar=t.bar),
            delta=-data['qty'] * data['item'].get_sell_price())

        return t

    def to_representation(self, transaction):
        obj = BaseTransactionSerializer(transaction, context={'ignore_type': True}).data
        if transaction is None:
            return obj

        iop = transaction.itemoperation_set.all()[0]
        obj["item"] = iop.target.id
        obj["qty"] = abs(iop.delta)

        aop = transaction.accountoperation_set.all()[0]
        obj["moneyflow"] = -aop.delta

        return obj


class ThrowTransactionSerializer(BaseTransactionSerializer, ItemQtySerializer):
    def create(self, data):
        t = super(ThrowTransactionSerializer, self).create(data)

        t.itemoperation_set.create(
            target=data["item"],
            delta=-data["qty"])

        return t

    def to_representation(self, transaction):
        obj = BaseTransactionSerializer(transaction, context={'ignore_type': True}).data
        if transaction is None:
            return obj

        iop = transaction.itemoperation_set.all()[0]
        obj["item"] = iop.target.id
        obj["qty"] = abs(iop.delta)

        obj["moneyflow"] = iop.delta * iop.target.get_sell_price()

        return obj


class DepositTransactionSerializer(BaseTransactionSerializer, AccountAmountSerializer):
    def create(self, data):
        t = super(DepositTransactionSerializer, self).create(data)

        t.accountoperation_set.create(
            target=data["account"],
            delta=data["amount"])
        t.accountoperation_set.create(
            target=get_default_account(t.bar),
            delta=data["amount"])

        return t

    def to_representation(self, transaction):
        obj = BaseTransactionSerializer(transaction, context={'ignore_type': True}).data
        if transaction is None:
            return obj

        aop = transaction.accountoperation_set.all()[0]
        obj["account"] = aop.target.id
        obj["amount"] = aop.delta

        obj["moneyflow"] = aop.delta

        return obj


class GiveTransactionSerializer(BaseTransactionSerializer, AccountAmountSerializer):
    def validate_account(self, account):
        account = super(GiveTransactionSerializer, self).validate_account(account)

        if self.context['request'].user == account.owner:
            raise serializers.ValidationError("Cannot give money to yourself")

        if self.context['request'].bar.id != account.bar.id:
            raise serializers.ValidationError("Cannot give across bars")

        return account

    def create(self, data):
        t = super(GiveTransactionSerializer, self).create(data)

        t.accountoperation_set.create(
            target=Account.objects.get(owner=t.author, bar=t.bar),
            delta=-data["amount"])
        t.accountoperation_set.create(
            target=data["account"],
            delta=data["amount"])

        return t

    def to_representation(self, transaction):
        obj = BaseTransactionSerializer(transaction, context={'ignore_type': True}).data
        if transaction is None:
            return obj

        from_op = transaction.accountoperation_set.all()[0]
        to_op = transaction.accountoperation_set.all()[1]
        if to_op.target.owner == transaction.author:
            from_op, to_op = to_op, from_op
        obj["account"] = to_op.target.id
        obj["amount"] = to_op.delta

        obj["moneyflow"] = to_op.delta

        return obj


class PunishTransactionSerializer(BaseTransactionSerializer, AccountAmountSerializer):
    motive = serializers.CharField()

    def create(self, data):
        t = super(PunishTransactionSerializer, self).create(data)

        t.accountoperation_set.create(
            target=data["account"],
            delta=-data["amount"])
        t.transactiondata_set.create(
            label='motive',
            data=data["motive"])

        return t

    def to_representation(self, transaction):
        obj = BaseTransactionSerializer(transaction, context={'ignore_type': True}).data
        if transaction is None:
            return obj

        aop = transaction.accountoperation_set.all()[0]
        obj["account"] = aop.target.id
        obj["amount"] = aop.delta

        data = transaction.transactiondata_set.all()[0]
        obj["motive"] = data.data

        obj["moneyflow"] = aop.delta

        return obj



class MealTransactionSerializer(BaseTransactionSerializer):
    items = ItemQtySerializer(many=True)
    accounts = AccountRatioSerializer(many=True)
    name = serializers.CharField(allow_blank=True)

    def create(self, data):
        t = super(MealTransactionSerializer, self).create(data)

        total_price = 0
        for i in data["items"]:
            t.itemoperation_set.create(
                target=i["item"],
                delta=-i["qty"])
            total_price += i["qty"] * i["item"].get_sell_price()

        total_ratio = 0
        for a in data["accounts"]:
            total_ratio += a["ratio"]
        for a in data["accounts"]:
            t.accountoperation_set.create(
                target=a["account"],
                delta=-total_price * a["ratio"] / total_ratio)

        t.transactiondata_set.create(
            label='name',
            data=data["name"])

        return t

    def to_representation(self, transaction):
        obj = BaseTransactionSerializer(transaction, context={'ignore_type': True}).data
        if transaction is None:
            return obj

        obj["items"] = []
        for iop in transaction.itemoperation_set.all():
            obj["items"].append({
                'item': iop.target.id,
                'qty': abs(iop.delta)
            })

        total_price = 0
        obj["accounts"] = []
        aops = transaction.accountoperation_set.all()
        for aop in aops:
            total_price += abs(aop.delta)
        for aop in aops:
            obj["accounts"].append({
                'account': aop.target.id,
                'ratio': abs(aop.delta) / total_price
            })

        data = transaction.transactiondata_set.all()[0]
        obj[data.label] = data.data

        obj["moneyflow"] = total_price

        return obj


class ApproTransactionSerializer(BaseTransactionSerializer):
    items = ItemQtyPriceSerializer(many=True)

    def create(self, data):
        t = super(ApproTransactionSerializer, self).create(data)

        total = 0
        for i in data["items"]:
            item = i["item"]
            if "price" in i:
                item.buy_price = i["price"] / i["qty"]
                item.save()
                total += i["price"]
            else:
                total += item.buy_price * i["qty"]

            t.itemoperation_set.create(
                target=item,
                delta=i["qty"])

        t.accountoperation_set.create(
            target=get_default_account(t.bar),
            delta=-total)

        return t

    def to_representation(self, transaction):
        obj = BaseTransactionSerializer(transaction, context={'ignore_type': True}).data
        if transaction is None:
            return obj

        obj["items"] = []
        for iop in transaction.itemoperation_set.all():
            obj["items"].append({
                'item': iop.target.id,
                'qty': abs(iop.delta)
            })

        aop = transaction.accountoperation_set.all()[0]
        obj["moneyflow"] = -aop.delta

        return obj


class InventoryTransactionSerializer(BaseTransactionSerializer):
    items = ItemQtySerializer(many=True)

    def create(self, data):
        t = super(InventoryTransactionSerializer, self).create(data)

        for i in data["items"]:
            t.itemoperation_set.create(
                target=i["item"],
                next_value=i["qty"],
                fixed=True)

        return t

    def to_representation(self, transaction):
        obj = BaseTransactionSerializer(transaction, context={'ignore_type': True}).data
        if transaction is None:
            return obj

        total_price = 0
        obj["items"] = []
        for iop in transaction.itemoperation_set.all():
            obj["items"].append({
                'item': iop.target.id,
                'qty': iop.delta
            })
            total_price += iop.delta * iop.target.get_sell_price()

        obj["moneyflow"] = total_price

        return obj




serializers_class_map = {
    "": BaseTransactionSerializer,
    "buy": BuyTransactionSerializer,
    "throw": ThrowTransactionSerializer,
    "deposit": DepositTransactionSerializer,
    "give": GiveTransactionSerializer,
    "punish": PunishTransactionSerializer,
    "meal": MealTransactionSerializer,
    "appro": ApproTransactionSerializer,
    "inventory": InventoryTransactionSerializer}
