from rest_framework.test import APITestCase

from bars_core.models.user import User
from bars_core.models.role import Role
from bars_core.models.bar import Bar
from bars_base.models.item import Item
from bars_base.models.account import Account
from bars_transactions.models import Transaction


class TransactionTests(APITestCase):
    def setUp(self):
        self.bar = Bar.objects.create(id='natationjone')
        self.bar2 = Bar.objects.create(id='natationrouge')

        self.user = User.objects.create(username='nadrieril')
        Account.objects.create(bar=self.bar, owner=self.user)

        self.user2 = User.objects.create(username='ntag')
        Account.objects.create(bar=self.bar, owner=self.user2)

        self.user3 = User.objects.create(username='tizot')
        Role.objects.create(name='staff', bar=self.bar, user=self.user3)
        Account.objects.create(bar=self.bar, owner=self.user3)

        self.user4 = User.objects.create(username='marioyc')
        Role.objects.create(name='staff', bar=self.bar2, user=self.user4)
        Account.objects.create(bar=self.bar2, owner=self.user4)

        Item.objects.create(name='Chocolat', bar=self.bar, price=1)

        Transaction.objects.create(bar=self.bar, author=self.user)

        Transaction.objects.create(bar=self.bar2, author=self.user4)


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
        Role.objects.create(name='staff', bar=self.bar, user=self.user4)
        Account.objects.create(bar=self.bar, owner=self.user4)
        self.client.force_authenticate(user=self.user4)

        response = self.client.put('/transaction/1/cancel/', {})
        self.assertEqual(response.status_code, 200)
        transaction = Transaction.objects.get(pk=1)
        self.assertTrue(transaction.canceled)

        response2 = self.client.put('/transaction/2/cancel/', {})
        self.assertEqual(response2.status_code, 200)
        transaction2 = Transaction.objects.get(pk=2)
        self.assertTrue(transaction2.canceled)


    def test_create_buytransaction(self):
        data = {'type':'buy', 'item':1, 'qty':1}
        start_qty = Item.objects.get(id=1).qty

        self.client.force_authenticate(user=self.user)
        response = self.client.post('/transaction/?bar=natationjone', data)
        self.assertEqual(response.status_code, 201)

        end_qty = Item.objects.get(id=1).qty
        self.assertEqual(end_qty, start_qty - 1)

    def test_create_buytransaction_itemdeleted(self):
        i = Item.objects.create(name='Pizza', bar=self.bar, price=1, deleted=True)
        data = {'type':'buy', 'item':i.id, 'qty':1}

        self.client.force_authenticate(user=self.user)
        response = self.client.post('/transaction/?bar=natationjone', data)
        self.assertEqual(response.status_code, 400)

    def test_create_buytransaction_wrong_bar(self):
        i = Item.objects.create(name='steak', bar=self.bar2, price=2)
        start_qty = i.qty

        data = {'type':'buy', 'item':i.id, 'qty':2}

        self.client.force_authenticate(user=self.user3)
        response = self.client.post('/transaction/?bar=natationrouge', data)
        self.assertEqual(response.status_code, 403)

        end_qty = Item.objects.get(id=i.id).qty
        self.assertEqual(end_qty, start_qty)

    def test_create_cancel_buytransaction(self):
        data = {'type':'buy', 'item':1, 'qty':1}
        start_qty = Item.objects.get(id=1).qty

        self.client.force_authenticate(user=self.user)

        response = self.client.post('/transaction/?bar=natationjone', data)
        self.assertEqual(response.status_code, 201)
        end_qty = Item.objects.get(id=1).qty
        self.assertEqual(end_qty, start_qty - 1)

        response2 = self.client.put('/transaction/3/cancel/', {})
        self.assertEqual(response.status_code, 200)
        end_qty = Item.objects.get(id=1).qty
        self.assertEqual(end_qty, start_qty)

        response3 = self.client.put('/transaction/3/cancel/', {})
        self.assertEqual(response.status_code, 200)
        end_qty = Item.objects.get(id=1).qty
        self.assertEqual(end_qty, start_qty)
