from rest_framework.test import APITestCase

from bars_core.models.user import User
from bars_core.models.role import Role
from bars_core.models.bar import Bar
from bars_base.models.item import Item, ItemDetails
from bars_base.models.account import Account


from mock import Mock
from serializers import (BaseTransactionSerializer, BuyTransactionSerializer, GiveTransactionSerializer,
                        ThrowTransactionSerializer, DepositTransactionSerializer,PunishTransactionSerializer,
                        MealTransactionSerializer, ApproTransactionSerializer, InventoryTransactionSerializer,)
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

        self.itemdetail, _ = ItemDetails.objects.get_or_create(name='Pizza')
        self.item, _ = Item.objects.get_or_create(details=self.itemdetail, bar=self.bar, price=1, tax=0.2)
        self.item.qty = 5
        self.item.save()

        self.itemdetail2, _ = ItemDetails.objects.get_or_create(name='Steak')
        self.item2, _ = Item.objects.get_or_create(details=self.itemdetail2, bar=self.bar, price=2, tax=0.1)
        self.item2.qty = 10
        self.item2.save()

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

        self.itemdetail.delete()
        self.item.delete()
        self.itemdetail2.delete()
        self.item2.delete()


class BuySerializerTests(SerializerTests):
    def test_buy(self):
        data = {'type':'buy', 'item':self.item.id, 'qty':3}
        s = BuyTransactionSerializer(data=data, context=self.context)
        self.assertTrue(s.is_valid())
        s.save()

        self.assertEqual(reload(self.item).qty, self.item.qty - data['qty'])
        self.assertEqual(reload(self.account).money, self.account.money - self.item.get_sell_price() * data['qty'])

    def test_buy_itemdeleted(self):
        deleted_item, _ = Item.objects.get_or_create(details=self.itemdetail, bar=self.bar, price=1, deleted=True)
        data = {'type':'buy', 'item':deleted_item.id, 'qty':3}
        s = BuyTransactionSerializer(data=data, context=self.context)

        with self.assertRaises(serializers.ValidationError) as err:
            s.is_valid(raise_exception=True)
        self.assertEqual(err.exception.detail, {'item': ['Item is deleted']})

    def test_buy_other_bar(self):
        wrong_item, _ = Item.objects.get_or_create(details=self.itemdetail, bar=self.wrong_bar, price=1)
        data = {'type':'buy', 'item':wrong_item.id, 'qty':3}
        s = BuyTransactionSerializer(data=data, context=self.context)

        with self.assertRaises(serializers.ValidationError) as err:
            s.is_valid(raise_exception=True)
        self.assertEqual(err.exception.detail, {'item': ['Cannot buy across bars']})


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
        data = {'type':'throw', 'item':self.item.id, 'qty':1}

        s = ThrowTransactionSerializer(data=data, context=self.context)
        self.assertTrue(s.is_valid())
        s.save()

        self.assertEqual(reload(self.item).qty, self.item.qty - 1)

    def test_thow_other_bar(self):
        self.context = {'request': Mock(user=self.user, bar=self.wrong_bar)}
        data = {'type':'throw', 'item':self.item.id, 'qty':1}

        s = ThrowTransactionSerializer(data=data, context=self.context)
        self.assertTrue(s.is_valid())

        with self.assertRaises(exceptions.PermissionDenied):
            s.save()
        self.assertEqual(reload(self.item).qty, self.item.qty)

    def test_throw_negative(self):
        data = {'type':'throw', 'item':self.item.id, 'qty':-1}

        s = ThrowTransactionSerializer(data=data, context=self.context)
        self.assertFalse(s.is_valid())


from bars_base.models.account import get_default_account


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

        self.assertEqual(reload(self.account).money,self.account.money + data['amount'])
        self.assertEqual(reload(self.bar_account).money,self.bar_account.money + data['amount'])

    def test_deposit_no_staff(self):
        data = {'type':'deposit', 'account':self.account.id, 'amount':40}

        s = DepositTransactionSerializer(data=data, context=self.context)
        self.assertTrue(s.is_valid())

        with self.assertRaises(exceptions.PermissionDenied):
            s.save()
        self.assertEqual(reload(self.account).money,self.account.money)
        self.assertEqual(reload(self.bar_account).money,self.bar_account.money)

    def test_deposit_other_bar(self):
        data = {'type':'deposit','account':self.wrong_account.id,'amount':30}

        s = DepositTransactionSerializer(data=data, context=self.context)
        self.assertTrue(s.is_valid(raise_exception=True))

        with self.assertRaises(exceptions.PermissionDenied):
            s.save()
        self.assertEqual(reload(self.wrong_account).money,self.wrong_account.money)
        self.assertEqual(reload(self.wrong_bar_account).money,self.wrong_bar_account.money)

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

        self.assertEqual(reload(self.account).money,self.account.money - data['amount'])

    def test_punish_no_staff(self):
        data = {'type':'punish', 'account':self.account.id, 'amount':50, 'motive':'vaisselle'}

        s = PunishTransactionSerializer(data=data, context=self.context)
        self.assertTrue(s.is_valid())

        with self.assertRaises(exceptions.PermissionDenied):
            s.save()
        self.assertEqual(reload(self.account).money,self.account.money)

    def test_punish_negative(self):
        data = {'type':'punish', 'account':self.account.id, 'amount':-50, 'motive':'cadeau'}

        s = PunishTransactionSerializer(data=data, context=self.context)
        self.assertFalse(s.is_valid())


class MealSerializerTests(SerializerTests):
    @classmethod
    def setUpClass(self):
        super(MealSerializerTests, self).setUpClass()

        self.user2, _ = User.objects.get_or_create(username='user2')
        self.account2, _ = Account.objects.get_or_create(bar=self.bar, owner=self.user2)
        self.account2.money = 500
        self.account2.save()


    def test_meal(self):
        data = {'type':'meal', 'name':'',
                'items': [
                    {'item':self.item.id, 'qty':5}
                ],'accounts': [
                    {"account":self.account.id,"ratio":1},
                ]
                }

        s = MealTransactionSerializer(data=data, context=self.context)
        self.assertTrue(s.is_valid())
        s.save()

        self.assertEqual(reload(self.item).qty,self.item.qty - data['items'][0]['qty'])
        end_money = self.account.money - data['items'][0]['qty'] * self.item.get_sell_price()
        self.assertEqual(reload(self.account).money,end_money)

    def test_meal_multiple(self):
        self.account2
        data = {'type':'meal', 'name':'',
                'items': [
                    {'item':self.item.id, 'qty':1},
                    {'item':self.item2.id, 'qty':5}
                ],'accounts': [
                    {'account':self.account.id, 'ratio':1.0},
                    {'account':self.account2.id, 'ratio':12.0}
                ]
                }

        s = MealTransactionSerializer(data=data, context=self.context)
        self.assertTrue(s.is_valid())
        s.save()

        self.assertEqual(reload(self.item).qty,self.item.qty - data['items'][0]['qty'])
        self.assertEqual(reload(self.item2).qty,self.item2.qty - data['items'][1]['qty'])

        total_money = data['items'][0]['qty'] * self.item.get_sell_price()
        total_money += data['items'][1]['qty'] * self.item2.get_sell_price()

        total_ratio = data['accounts'][0]['ratio'] + data['accounts'][1]['ratio']

        end_money = self.account.money - total_money * data['accounts'][0]['ratio'] / total_ratio
        end_money2 = self.account2.money - total_money * data['accounts'][1]['ratio'] / total_ratio

        self.assertEqual(reload(self.account).money,end_money)
        self.assertEqual(reload(self.account2).money,end_money2)


class ApproSerializerTests(SerializerTests):
    @classmethod
    def setUpClass(self):
        super(ApproSerializerTests, self).setUpClass()

        self.bar_account = get_default_account(self.bar)


    def test_appro(self):
        self.context = {'request': Mock(user=self.staff_user, bar=self.bar)}
        data = {'type':'appro',
                'items': [
                    {'item':self.item.id, 'qty':10},
                    {'item':self.item2.id, 'qty':100, 'price':250}
                ]
                }

        s = ApproTransactionSerializer(data=data, context=self.context)
        self.assertTrue(s.is_valid())
        s.save()

        self.assertEqual(reload(self.item).qty,self.item.qty + data['items'][0]['qty'])
        self.assertEqual(reload(self.item2).qty,self.item2.qty + data['items'][1]['qty'])

        end_money = self.bar_account.money
        end_money -= data['items'][0]['qty'] * self.item.buy_price
        end_money -= data['items'][1]['price']

        self.assertEqual(reload(self.bar_account).money,end_money)

    def test_appro_no_staff(self):
        data = {'type':'appro',
                'items': [
                    {'item':self.item.id, 'qty':10}
                ]
                }

        s = ApproTransactionSerializer(data=data, context=self.context)
        self.assertTrue(s.is_valid())

        with self.assertRaises(exceptions.PermissionDenied):
            s.save()

        self.assertEqual(reload(self.item).qty,self.item.qty)
        self.assertEqual(reload(self.bar_account).money,self.bar_account.money)


class InventorySerializerTests(SerializerTests):
    def test_inventory(self):
        self.context = {'request': Mock(user=self.staff_user, bar=self.bar)}
        data = {'type':'inventory',
                'items': [
                    {'item':self.item.id, 'qty':3},
                    {'item':self.item2.id, 'qty': 5}
                ]
                }

        s = InventoryTransactionSerializer(data=data, context=self.context)
        self.assertTrue(s.is_valid())
        s.save()

        self.assertEqual(reload(self.item).qty, data['items'][0]['qty'])
        self.assertEqual(reload(self.item2).qty, data['items'][1]['qty'])

    def test_inventory_no_staff(self):
        self.context = {'request': Mock(user=self.user, bar=self.bar)}
        data = {'type':'inventory',
                'items': [
                    {'item':self.item.id, 'qty':1},
                    {'item':self.item2.id, 'qty': 7}
                ]
                }

        s = InventoryTransactionSerializer(data=data, context=self.context)
        self.assertTrue(s.is_valid())

        with self.assertRaises(exceptions.PermissionDenied):
            s.save()

        self.assertEqual(reload(self.item).qty, self.item.qty)
        self.assertEqual(reload(self.item2).qty, self.item2.qty)
