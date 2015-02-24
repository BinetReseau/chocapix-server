from django.http import Http404
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework import exceptions

from bars_base.models.account import Account, get_default_account
from bars_items.models.buyitem import BuyItem, BuyItemPrice
from bars_items.models.stockitem import StockItem
from bars_items.models.sellitem import SellItem
from bars_transactions.models import Transaction

ERROR_MESSAGES = {
    'negative': "%(field)s must be positive",
    'wrong_bar': "%(model)s (id=%(id)d) is in the wrong bar",
    'deleted': "%(model)s (id=%(id)d) is deleted"
}

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
    stockitem = serializers.PrimaryKeyRelatedField(queryset=StockItem.objects.all(), required=False)
    sellitem = serializers.PrimaryKeyRelatedField(queryset=SellItem.objects.all(), required=False)
    qty = serializers.FloatField()

    def validate_qty(self, value):
        if value < 0:
            raise ValidationError(ERROR_MESSAGES['negative'] % {'field':"Quantity"})
        return value

    def validate_stockitem(self, item):
        err_params = {'model':'StockItem', 'id':item.id}
        if item is not None and item.deleted:
            raise ValidationError(ERROR_MESSAGES['deleted'] % err_params)

        if item is not None and self.context['request'].bar.id != item.bar.id:
            raise ValidationError(ERROR_MESSAGES['wrong_bar'] % err_params)

        return item

    def validate_sellitem(self, item):
        err_params = {'model':'SellItem', 'id':item.id}
        if item is not None and item.deleted:
            raise ValidationError(ERROR_MESSAGES['deleted'] % err_params)

        if item is not None and self.context['request'].bar.id != item.bar.id:
            raise ValidationError(ERROR_MESSAGES['wrong_bar'] % err_params)

        return item

    def validate(self, data):
        if "stockitem" in data and "sellitem" in data:
            raise ValidationError("Two items were given")
        if "stockitem" not in data and "sellitem" not in data:
            raise ValidationError("No items were given")
        return data


    def create(self, data):
        t = self.context['transaction']
        qty = data['qty']

        if "stockitem" in data:
            stockitem = data['stockitem']
            stockitem.create_operation(delta=-qty, unit='sell', transaction=t)

            return qty * stockitem.get_price(unit='sell')

        elif "sellitem" in data:
            sellitem = data['sellitem']
            total_qty = sellitem.calc_qty()
            stockitems = sellitem.stockitems.all()

            total_price = 0
            for si in stockitems.all():
                if total_qty != 0:
                    delta = (si.qty * qty) / total_qty
                else:
                    delta = qty / stockitems.count()

                si.create_operation(delta=-delta, unit='sell', transaction=t, fuzzy=True)
                total_price += delta * si.get_price(unit='sell')

            return total_price

    @staticmethod
    def serializeOperations(iops, force_fuzzy=True):
        stockitems = []
        sellitem_map = {}
        for iop in iops:
            stockitem = iop.target
            delta = iop.delta / stockitem.get_unit('sell')
            if iop.fuzzy or force_fuzzy:
                sellitem = stockitem.sellitem
                if sellitem.id not in sellitem_map:
                    sellitem_map[sellitem.id] = {'sellitem':sellitem.id, 'qty':0}
                sellitem_map[sellitem.id]['qty'] += delta
            else:
                stockitems.append({'stockitem':stockitem.id, 'qty':delta})

        return stockitems + sellitem_map.values()


class BuyItemQtyPriceSerializer(serializers.Serializer):
    buyitem = serializers.PrimaryKeyRelatedField(queryset=BuyItem.objects.all())
    qty = serializers.FloatField()
    price = serializers.FloatField(required=False)

    def validate_qty(self, value):
        if value < 0:
            raise ValidationError("Quantity must be positive")
        return value

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
    def create(self, data):
        t = super(BuyTransactionSerializer, self).create(data)

        self.context["transaction"] = t
        money_delta = ItemQtySerializer.create(self, data)

        t.accountoperation_set.create(
            target=Account.objects.get(owner=t.author, bar=t.bar),
            delta=-money_delta)

        return t

    def to_representation(self, transaction):
        obj = BaseTransactionSerializer(transaction, context={'ignore_type': True}).data
        if transaction is None:
            return obj

        force_fuzzy = True
        obj["items"] = ItemQtySerializer.serializeOperations(transaction.itemoperation_set.select_related(), force_fuzzy)

        aop = transaction.accountoperation_set.all()[0]
        obj["moneyflow"] = -aop.delta

        return obj


class ThrowTransactionSerializer(BaseTransactionSerializer, ItemQtySerializer):
    def create(self, data):
        t = super(ThrowTransactionSerializer, self).create(data)
        stockitem = data['stockitem']
        qty = data['qty']

        stockitem.create_operation(delta=-qty, unit='sell', transaction=t)

        return t

    def to_representation(self, transaction):
        obj = BaseTransactionSerializer(transaction, context={'ignore_type': True}).data
        if transaction is None:
            return obj

        iop = transaction.itemoperation_set.all()[0]
        stockitem = iop.target
        obj["stockitem"] = stockitem.id
        obj["qty"] = -iop.delta / stockitem.get_unit('sell')

        obj["moneyflow"] = iop.delta * stockitem.get_price()

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

        s = ItemQtySerializer()
        s.context["transaction"] = t

        total_price = 0
        for i in data["items"]:
            total_price += ItemQtySerializer.create(s, i)

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

        force_fuzzy = True
        obj["items"] = ItemQtySerializer.serializeOperations(transaction.itemoperation_set.select_related(), force_fuzzy)

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
    items = BuyItemQtyPriceSerializer(many=True)

    def create(self, data):
        t = super(ApproTransactionSerializer, self).create(data)

        stockitem_map = {}
        total = 0
        for i in data["items"]:
            buyitem = i["buyitem"]
            qty = i["qty"] * buyitem.itemqty
            priceobj, _ = BuyItemPrice.objects.get_or_create(bar=t.bar, buyitem=buyitem)
            if "price" in i:
                priceobj.price = i["price"] / qty
                priceobj.save()
                total += i["price"]
            else:
                total += priceobj.price * qty

            stockitem = StockItem.objects.get(bar=t.bar, details=buyitem.details)
            if stockitem.id not in stockitem_map:
                stockitem_map[stockitem.id] = {'stockitem': stockitem, 'delta': 0}
            stockitem_map[stockitem.id]['delta'] += qty * stockitem.get_unit('buy')

        for x in stockitem_map.values():
            x['stockitem'].create_operation(delta=x['delta'], unit='buy', transaction=t)

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
                'stockitem': iop.target.id,
                'qty': iop.delta * iop.target.get_unit('sell')
            })

        aop = transaction.accountoperation_set.all()[0]
        obj["moneyflow"] = -aop.delta

        return obj


class InventoryTransactionSerializer(BaseTransactionSerializer):
    items = ItemQtySerializer(many=True)

    def create(self, data):
        t = super(InventoryTransactionSerializer, self).create(data)

        for i in data["items"]:
            i["stockitem"].create_operation(next_value=i["qty"], unit='sell', transaction=t, fixed=True)

        return t

    def to_representation(self, transaction):
        obj = BaseTransactionSerializer(transaction, context={'ignore_type': True}).data
        if transaction is None:
            return obj

        total_price = 0
        obj["items"] = []
        for iop in transaction.itemoperation_set.all():
            obj["items"].append({
                'stockitem': iop.target.id,
                'qty': iop.delta
            })
            total_price += iop.delta * iop.target.sell_price

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
