from rest_framework.test import APITestCase

from bars_core.models.user import User
from bars_core.models.role import Role
from bars_core.models.bar import Bar
from bars_base.models.item import Item, ItemDetails
from bars_base.models.account import Account
from bars_transactions.models import Transaction


class TransactionTests(APITestCase):
    def setUp(self):
        self.bar = Bar.objects.create(id='natationjone')

        self.user = User.objects.create(username='nadrieril')
        Account.objects.create(bar=self.bar, owner=self.user)

        self.user2 = User.objects.create(username='ntag')
        Account.objects.create(bar=self.bar, owner=self.user2)

        self.user3 = User.objects.create(username='tizot')
        Role.objects.create(name='staff', bar=self.bar, user=self.user3)
        Account.objects.create(bar=self.bar, owner=self.user3)

        itemdetails = ItemDetails.objects.create(name='Chocolat')
        Item.objects.create(details=itemdetails, bar=self.bar, price=1)

        self.client.force_authenticate(user=self.user)
        Transaction.objects.create(bar=self.bar, author=self.user)


    def test_cancel_transaction(self):
        response = self.client.put('/transaction/1/cancel/?bar=natationjone', {})
        self.assertEqual(response.status_code, 200)
        transaction = Transaction.objects.get(pk=1)
        self.assertEqual(transaction.canceled, True)

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


    def test_create_buytransaction(self):
        data = {'type':'buy', 'item':1, 'qty':1}
        start_qty = Item.objects.get(id=1).qty

        self.client.force_authenticate(user=self.user)
        response = self.client.post('/transaction/?bar=natationjone', data)
        self.assertEqual(response.status_code, 201)

        end_qty = Item.objects.get(id=1).qty
        self.assertEqual(end_qty, start_qty - 1)
