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

        self.user = User.objects.create(username='nadrieril')
        Account.objects.create(bar=self.bar, owner=self.user)

        self.user2 = User.objects.create(username='ntag')
        Account.objects.create(bar=self.bar, owner=self.user2)

        self.user3 = User.objects.create(username='tizot')
        Role.objects.create(name='staff', bar=self.bar, user=self.user3)
        Account.objects.create(bar=self.bar, owner=self.user3)

        Item.objects.create(name='Chocolat', bar=self.bar, price=1)

        self.client.force_authenticate(user=self.user)
        transaction = {'type':'buy', 'item':1, 'qty':1}
        self.client.post('/transaction/?bar=natationjone', transaction)

    def test_cancel_transaction(self):
        response = self.client.put('/transaction/1/cancel/?bar=natationjone', {})
        self.assertEqual(response.status_code, 200)
        transaction = Transaction.objects.get(pk=1)
        self.assertEqual(transaction.canceled, True)

        response = self.client.put('/transaction/1/restore/?bar=natationjone', {})
        self.assertEqual(response.status_code, 200)
        transaction = Transaction.objects.get(pk=1)
        self.assertEqual(transaction.canceled, False)

        self.client.force_authenticate(user=self.user2)
        response = self.client.put('/transaction/1/cancel/?bar=natationjone', {})
        self.assertEqual(response.status_code, 403)

        self.client.force_authenticate(user=self.user3)
        response = self.client.put('/transaction/1/cancel/?bar=natationjone', {})
        self.assertEqual(response.status_code, 200)
