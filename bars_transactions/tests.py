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

        self.client.force_authenticate(user=self.user)
        Transaction.objects.create(bar=self.bar, author=self.user)

        Transaction.objects.create(bar=self.bar2, author=self.user4)


    def test_cancel_transaction(self):
        response = self.client.put('/transaction/1/cancel/?bar=natationjone', {})
        self.assertEqual(response.status_code, 200)
        transaction = Transaction.objects.get(pk=1)
        self.assertEqual(transaction.canceled, True)

    def test_cancel_transaction_unexisting_bar(self):
        response = self.client.put('/transaction/1/cancel/?bar=basketjone', {})
        self.assertEqual(response.status_code, 404)

    def test_cancel_unexisting_transaction(self):
        response = self.client.put('/transaction/3/cancel/?bar=natationjone', {})
        self.assertEqual(response.status_code, 404)

    def test_restore_transaction(self):
        response = self.client.put('/transaction/1/restore/?bar=natationjone', {})
        self.assertEqual(response.status_code, 200)
        transaction = Transaction.objects.get(pk=1)
        self.assertEqual(transaction.canceled, False)

    def test_cancel_transaction_wrong_user(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.put('/transaction/1/cancel/?bar=natationjone', {})
        self.assertEqual(response.status_code, 403)

    def test_cancel_transaction_staff(self):
        self.client.force_authenticate(user=self.user3)
        response = self.client.put('/transaction/1/cancel/?bar=natationjone', {})
        self.assertEqual(response.status_code, 200)

    def test_cancel_transaction_staff_wrong_bar(self):
        self.client.force_authenticate(user=self.user3)
        response = self.client.put('/transaction/1/cancel/?bar=natationrouge', {})
        self.assertEqual(response.status_code, 403)

    def test_create_buytransaction(self):
        data = {'type':'buy', 'item':1, 'qty':1}
        start_qty = Item.objects.get(id=1).qty

        self.client.force_authenticate(user=self.user)
        response = self.client.post('/transaction/?bar=natationjone', data)
        self.assertEqual(response.status_code, 201)

        end_qty = Item.objects.get(id=1).qty
        self.assertEqual(end_qty, start_qty - 1)
        self.assertTrue(end_qty >= 0)

    def test_create_buytransaction_itemdeleted(self):
        i = Item.objects.create(name='Pizza', bar=self.bar, price=1, deleted=True)
        data = {'type':'buy', 'item':i.id, 'qty':1}

        self.client.force_authenticate(user=self.user)
        response = self.client.post('/transaction/?bar=natationjone', data)
        self.assertEqual(response.status_code, 400)
