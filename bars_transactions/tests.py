from rest_framework.test import APITestCase

from bars_core.models.user import User
from bars_core.models.role import Role
from bars_core.models.bar import Bar
from bars_base.models.item import Item, ItemDetails
from bars_base.models.account import Account
from bars_transactions.models import Transaction


class TransactionTests(APITestCase):
    def setUp(self):
        self.bar, _ = Bar.objects.get_or_create(id='natationjone')
        self.bar2, _ = Bar.objects.get_or_create(id='natationrouge')

        self.user, _ = User.objects.get_or_create(username='nadrieril')
        Account.objects.get_or_create(bar=self.bar, owner=self.user)

        self.user2, _ = User.objects.get_or_create(username='ntag')
        Account.objects.get_or_create(bar=self.bar, owner=self.user2)

        self.user3, _ = User.objects.get_or_create(username='tizot')
        Role.objects.get_or_create(name='staff', bar=self.bar, user=self.user3)
        Account.objects.get_or_create(bar=self.bar, owner=self.user3)

        self.user4, _ = User.objects.get_or_create(username='marioyc')
        Role.objects.get_or_create(name='staff', bar=self.bar2, user=self.user4)
        Account.objects.get_or_create(bar=self.bar2, owner=self.user4)

        itemdetails, _ = ItemDetails.objects.get_or_create(name='Chocolat')
        self.item, _ = Item.objects.get_or_create(details=itemdetails, bar=self.bar, price=1)

        Transaction.objects.get_or_create(bar=self.bar, author=self.user)

        Transaction.objects.get_or_create(bar=self.bar2, author=self.user4)


    def test_cancel_transaction(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put('/transaction/1/cancel/', {})
        self.assertEqual(response.status_code, 200)
        transaction = Transaction.objects.get(pk=1)
        self.assertTrue(transaction.canceled)

    def test_cancel_unexisting_transaction(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put('/transaction/3/cancel/', {})
        self.assertEqual(response.status_code, 404)

    def test_restore_transaction(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put('/transaction/1/restore/', {})
        self.assertEqual(response.status_code, 200)
        transaction = Transaction.objects.get(pk=1)
        self.assertFalse(transaction.canceled)

    def test_cancel_transaction_wrong_user(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.put('/transaction/1/cancel/', {})
        self.assertEqual(response.status_code, 403)
        transaction = Transaction.objects.get(pk=1)
        self.assertFalse(transaction.canceled)

    def test_cancel_transaction_staff(self):
        self.client.force_authenticate(user=self.user3)
        response = self.client.put('/transaction/1/cancel/', {})
        self.assertEqual(response.status_code, 200)
        transaction = Transaction.objects.get(pk=1)
        self.assertTrue(transaction.canceled)

    def test_cancel_transaction_staff_wrong_bar(self):
        self.client.force_authenticate(user=self.user3)
        response = self.client.put('/transaction/2/cancel/', {})
        self.assertEqual(response.status_code, 403)
        transaction = Transaction.objects.get(pk=2)
        self.assertFalse(transaction.canceled)

    def test_cancel_transaction_two_bars(self):
        Role.objects.get_or_create(name='staff', bar=self.bar, user=self.user4)
        Account.objects.get_or_create(bar=self.bar, owner=self.user4)
        self.client.force_authenticate(user=self.user4)

        response = self.client.put('/transaction/1/cancel/', {})
        self.assertEqual(response.status_code, 200)
        transaction = Transaction.objects.get(pk=1)
        self.assertTrue(transaction.canceled)

        response2 = self.client.put('/transaction/2/cancel/', {})
        self.assertEqual(response2.status_code, 200)
        transaction2 = Transaction.objects.get(pk=2)
        self.assertTrue(transaction2.canceled)

    # TODO: move to operation tests
    def test_create_cancel_buytransaction(self):
        data = {'type':'buy', 'item':self.item.id, 'qty':1}
        start_qty = Item.objects.get(id=self.item.id).qty

        self.client.force_authenticate(user=self.user)

        response = self.client.post('/transaction/?bar=natationjone', data)
        self.assertEqual(response.status_code, 201)
        end_qty = Item.objects.get(id=self.item.id).qty
        self.assertEqual(end_qty, start_qty - 1)

        response2 = self.client.put('/transaction/3/cancel/', {})
        self.assertEqual(response2.status_code, 200)
        end_qty = Item.objects.get(id=self.item.id).qty
        self.assertEqual(end_qty, start_qty)

        response3 = self.client.put('/transaction/3/cancel/', {})
        self.assertEqual(response3.status_code, 200)
        end_qty = Item.objects.get(id=self.item.id).qty
        self.assertEqual(end_qty, start_qty)


from mock import Mock
from serializers import BaseTransactionSerializer, BuyTransactionSerializer, GiveTransactionSerializer
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

        self.context = {'request': Mock(user=self.user, QUERY_PARAMS={'bar': self.bar.id})}
        self.context_wrong_bar = {'request': Mock(user=self.user, QUERY_PARAMS={'bar': self.wrong_bar.id})}
        self.context_no_bar = {'request': Mock(user=self.user, QUERY_PARAMS={})}

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

        self.itemdetail, _ = ItemDetails.objects.get_or_create(name='Pizza')
        self.item, _ = Item.objects.get_or_create(details=self.itemdetail, bar=self.bar, price=1)
        self.item.qty = 5
        self.item.save()

        self.context = {'request': Mock(user=self.user, QUERY_PARAMS={'bar': self.bar.id})}

    @classmethod
    def tearDownClass(self):
        self.bar.delete()
        self.wrong_bar.delete()

        self.user.delete()
        self.account.delete()
        self.wrong_user.delete()
        self.wrong_account.delete()

        self.itemdetail.delete()
        self.item.delete()


class BuySerializerTests(SerializerTests):
    def test_buy(self):
        data = {'type':'buy', 'item':self.item.id, 'qty':3}
        s = BuyTransactionSerializer(data=data, context=self.context)
        self.assertTrue(s.is_valid())
        s.save()

        self.assertEqual(reload(self.item).qty, self.item.qty - data['qty'])
        self.assertEqual(reload(self.account).money, self.account.money - self.item.price * data['qty'])

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
