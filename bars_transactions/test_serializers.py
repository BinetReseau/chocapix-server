from rest_framework.test import APITestCase

from bars_core.models.bar import Bar
from bars_core.models.user import User
from bars_core.models.role import Role
from bars_core.models.account import Account

from bars_items.models.buyitem import BuyItem, BuyItemPrice
from bars_items.models.itemdetails import ItemDetails
from bars_items.models.sellitem import SellItem
from bars_items.models.stockitem import StockItem

from bars_transactions.models import Transaction



from mock import Mock
from serializers import (BaseTransactionSerializer, BuyTransactionSerializer, GiveTransactionSerializer,
                         ThrowTransactionSerializer, DepositTransactionSerializer, PunishTransactionSerializer,)
from django.http import Http404
from rest_framework import exceptions, serializers


def reload(obj):
    return obj.__class__.objects.get(pk=obj.pk)


class BaseSerializerTests(APITestCase):
    @classmethod
    def setUpClass(self):
        self.bar, _ = Bar.objects.get_or_create(id='barjone')
        self.wrong_bar, _ = Bar.objects.get_or_create(id='barrouje')

        self.user, _ = User.objects.get_or_create(username='user')
        self.user.has_perm = Mock(side_effect=lambda perm, bar: bar.id == self.bar.id)

        self.context = {'request': Mock(user=self.user, bar=self.bar)}
        self.context_wrong_bar = {'request': Mock(user=self.user, bar=self.wrong_bar)}
        self.context_no_bar = {'request': Mock(user=self.user, bar=None)}

        self.data = {'type': 'some_type'}

    def test_base_transaction(self):
        s = BaseTransactionSerializer(data=self.data, context=self.context)
        self.assertTrue(s.is_valid())
        t = s.save()

        self.assertEqual(t.bar.id, self.bar.id)

    def test_base_transaction_wrong_bar(self):
        s = BaseTransactionSerializer(data=self.data, context=self.context_wrong_bar)
        self.assertTrue(s.is_valid())

        with self.assertRaises(exceptions.PermissionDenied):
            s.save()

    def test_base_transaction_no_bar(self):
        s = BaseTransactionSerializer(data=self.data, context=self.context_no_bar)
        self.assertTrue(s.is_valid())

        with self.assertRaises(Http404):
            s.save()


class SerializerTests(APITestCase):
    @classmethod
    def setUpClass(self):
        self.bar, _ = Bar.objects.get_or_create(id='barjone')
        self.wrong_bar, _ = Bar.objects.get_or_create(id='barrouje')

        self.user, _ = User.objects.get_or_create(username='user')
        self.account, _ = Account.objects.get_or_create(bar=self.bar, owner=self.user)
        self.account.money = 100
        self.account.save()
        self.wrong_user, _ = User.objects.get_or_create(username='wrong_user')
        self.wrong_account, _ = Account.objects.get_or_create(bar=self.wrong_bar, owner=self.wrong_user)

        self.staff_user, _ = User.objects.get_or_create(username='staff_user')
        self.staff_account, _ = Account.objects.get_or_create(bar=self.bar, owner=self.staff_user)
        self.staff_role, _ = Role.objects.get_or_create(name='staff', bar=self.bar, user=self.staff_user)

        self.sellitem, _ = SellItem.objects.get_or_create(bar=self.bar, name="Chocolat", tax=0.2)
        self.itemdetails, _ = ItemDetails.objects.get_or_create(name="Chocolat")
        self.buyitem, _ = BuyItem.objects.get_or_create(details=self.itemdetails)
        self.stockitem, _ = StockItem.objects.get_or_create(bar=self.bar, sellitem=self.sellitem, details=self.itemdetails, price=1)
        self.stockitem.unit_factor = 5
        self.stockitem.qty = 5
        self.stockitem.save()

        self.context = {'request': Mock(user=self.user, bar=self.bar)}

    @classmethod
    def tearDownClass(self):
        self.bar.delete()
        self.wrong_bar.delete()

        self.user.delete()
        self.account.delete()
        self.wrong_user.delete()
        self.wrong_account.delete()

        self.staff_user.delete()
        self.staff_account.delete()
        self.staff_role.delete()

        self.sellitem.delete()
        self.itemdetails.delete()
        self.buyitem.delete()
        self.stockitem.delete()


class BuySerializerTests(SerializerTests):
    def tearDown(self):
        self.stockitem.deleted = False
        self.stockitem.save()

    def test_buy(self):
        data = {'type':'buy', 'stockitem':self.stockitem.id, 'qty':3}
        s = BuyTransactionSerializer(data=data, context=self.context)
        self.assertTrue(s.is_valid())
        s.save()

        self.assertEqual(reload(self.stockitem).qty, self.stockitem.qty - data['qty'] * self.stockitem.get_unit('sell'))
        self.assertEqual(reload(self.account).money, self.account.money - data['qty'] * self.stockitem.sell_price)

    def test_buy_itemdeleted(self):
        self.stockitem.deleted = True
        self.stockitem.save()
        data = {'type':'buy', 'stockitem':self.stockitem.id, 'qty':3}
        s = BuyTransactionSerializer(data=data, context=self.context)

        with self.assertRaises(serializers.ValidationError) as err:
            s.is_valid(raise_exception=True)
        self.assertEqual(err.exception.detail, {'stockitem': ['StockItem (id=%d) is deleted' % self.stockitem.id]})

    def test_buy_other_bar(self):
        wrong_sellitem, _ = SellItem.objects.get_or_create(bar=self.wrong_bar, name="Lait", tax=0.1)
        wrong_stockitem, _ = StockItem.objects.get_or_create(bar=self.wrong_bar, details=self.itemdetails, sellitem=wrong_sellitem, price=1)

        data = {'type':'buy', 'stockitem':wrong_stockitem.id, 'qty':3}
        s = BuyTransactionSerializer(data=data, context=self.context)

        with self.assertRaises(serializers.ValidationError) as err:
            s.is_valid(raise_exception=True)
        self.assertEqual(err.exception.detail, {'stockitem': ['StockItem (id=%d) is in the wrong bar' % wrong_stockitem.id]})


class GiveSerializerTests(SerializerTests):
    @classmethod
    def setUpClass(self):
        super(GiveSerializerTests, self).setUpClass()
        self.user2, _ = User.objects.get_or_create(username='user2')
        self.account2, _ = Account.objects.get_or_create(bar=self.bar, owner=self.user2)

    @classmethod
    def tearDownClass(self):
        self.user2.delete()
        self.account2.delete()
        super(GiveSerializerTests, self).tearDownClass()


    def test_give(self):
        data = {'type':'give', 'account':self.account2.id, 'amount':10}
        s = GiveTransactionSerializer(data=data, context=self.context)
        self.assertTrue(s.is_valid())
        s.save()

        self.assertEqual(reload(self.account).money, self.account.money - data['amount'])
        self.assertEqual(reload(self.account2).money, self.account2.money + data['amount'])

    def test_give_other_bar(self):
        data = {'type':'give', 'account':self.wrong_account.id, 'amount':10}
        s = GiveTransactionSerializer(data=data, context=self.context)

        with self.assertRaises(serializers.ValidationError) as err:
            s.is_valid(raise_exception=True)
        self.assertEqual(err.exception.detail, {'account': ['Cannot give across bars']})


class ThrowSerializerTests(SerializerTests):
    def test_throw(self):
        data = {'type':'throw', 'stockitem':self.stockitem.id, 'qty':1}

        s = ThrowTransactionSerializer(data=data, context=self.context)
        self.assertTrue(s.is_valid())
        s.save()

        self.assertEqual(reload(self.stockitem).qty, self.stockitem.qty - data['qty'] * self.stockitem.get_unit('sell'))

    def test_throw_other_bar(self):
        context = {'request': Mock(user=self.user, bar=self.wrong_bar)}
        data = {'type':'throw', 'stockitem':self.stockitem.id, 'qty':1}

        s = ThrowTransactionSerializer(data=data, context=context)

        with self.assertRaises(serializers.ValidationError) as err:
            s.is_valid(raise_exception=True)
        self.assertEqual(err.exception.detail, {'stockitem': ['StockItem (id=%d) is in the wrong bar' % self.stockitem.id]})

    def test_throw_negative(self):
        data = {'type':'throw', 'stockitem':self.stockitem.id, 'qty':-1}

        s = ThrowTransactionSerializer(data=data, context=self.context)
        self.assertFalse(s.is_valid())


from bars_core.models.account import get_default_account

class DepositSerializerTests(SerializerTests):
    @classmethod
    def setUpClass(self):
        super(DepositSerializerTests, self).setUpClass()

        self.bar_account = get_default_account(self.bar)
        self.wrong_bar_account = get_default_account(self.wrong_bar)


    def test_deposit_staff(self):
        self.context = {'request': Mock(user=self.staff_user, bar=self.bar)}
        data = {'type':'deposit', 'account':self.account.id, 'amount':30}

        s = DepositTransactionSerializer(data=data, context=self.context)
        self.assertTrue(s.is_valid())
        s.save()

        self.assertEqual(reload(self.account).money, self.account.money + data['amount'])
        self.assertEqual(reload(self.bar_account).money, self.bar_account.money + data['amount'])

    def test_deposit_no_staff(self):
        data = {'type':'deposit', 'account':self.account.id, 'amount':40}

        s = DepositTransactionSerializer(data=data, context=self.context)
        self.assertTrue(s.is_valid())

        with self.assertRaises(exceptions.PermissionDenied):
            s.save()
        self.assertEqual(reload(self.account).money, self.account.money)
        self.assertEqual(reload(self.bar_account).money, self.bar_account.money)

    def test_deposit_other_bar(self):
        data = {'type':'deposit', 'account':self.wrong_account.id, 'amount':30}

        s = DepositTransactionSerializer(data=data, context=self.context)
        self.assertTrue(s.is_valid(raise_exception=True))

        with self.assertRaises(exceptions.PermissionDenied):
            s.save()
        self.assertEqual(reload(self.wrong_account).money, self.wrong_account.money)
        self.assertEqual(reload(self.wrong_bar_account).money, self.wrong_bar_account.money)

    def test_deposit_negative(self):
        self.context = {'request': Mock(user=self.staff_user, bar=self.bar)}
        data = {'type':'deposit', 'account':self.account.id, 'amount':-30}

        s = DepositTransactionSerializer(data=data, context=self.context)
        self.assertFalse(s.is_valid())

class PunishSerializerTests(SerializerTests):
    def test_punish(self):
        self.context = {'request': Mock(user=self.staff_user, bar=self.bar)}
        data = {'type':'punish', 'account':self.account.id, 'amount':50, 'motive':'vaisselle'}

        s = PunishTransactionSerializer(data=data, context=self.context)
        self.assertTrue(s.is_valid())
        s.save()

        self.assertEqual(reload(self.account).money, self.account.money - data['amount'])

    def test_punish_no_staff(self):
        data = {'type':'punish', 'account':self.account.id, 'amount':50, 'motive':'vaisselle'}

        s = PunishTransactionSerializer(data=data, context=self.context)
        self.assertTrue(s.is_valid())

        with self.assertRaises(exceptions.PermissionDenied):
            s.save()
        self.assertEqual(reload(self.account).money, self.account.money)

    def test_punish_negative(self):
        data = {'type':'punish', 'account':self.account.id, 'amount':-50, 'motive':'cadeau'}

        s = PunishTransactionSerializer(data=data, context=self.context)
        self.assertFalse(s.is_valid())
