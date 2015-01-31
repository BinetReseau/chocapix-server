from rest_framework.test import APITestCase

from bars_api.models.user import User
from bars_api.models.role import Role
from bars_api.models.bar import Bar
from bars_api.models.item import Item
from bars_api.models.account import Account
from bars_api.models.transaction import Transaction


class ItemTests(APITestCase):
    def test_get_item(self):
        response = self.client.get('/item/')
        self.assertEqual(response.data, [])


class ItemPermsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='nadrieril')
        self.bar = Bar.objects.create(id='natationjone')
        Bar.objects.create(id='avironjone')
        Item.objects.create(name='Chocolat', bar=self.bar, price=1)

    def test_create_item(self):
        data = {'name': 'test', 'qty': 0, 'bar': 'natationjone', 'price': 1}

        # Unauthenticated
        response = self.client.post('/item/?bar=natationjone', data)
        self.assertEqual(response.status_code, 401)

        # Wrong permissions
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/item/?bar=natationjone', data)
        self.assertEqual(response.status_code, 403)

        # Correct permissions
        Role.objects.create(name='appromanager', bar=self.bar, user=self.user)
        response = self.client.post('/item/?bar=natationjone', data)
        self.assertEqual(response.status_code, 201)

        # Wrong bar
        response = self.client.post('/item/?bar=avironjone', data)
        self.assertEqual(response.status_code, 403)


    def test_change_item(self):
        data = self.client.get('/item/1/').data
        data['name'] = "Pizza"

        # Unauthenticated
        response = self.client.put('/item/1/?bar=natationjone', data)
        self.assertEqual(response.status_code, 401)

        # Wrong permissions
        self.client.force_authenticate(user=self.user)
        response = self.client.put('/item/1/?bar=natationjone', data)
        self.assertEqual(response.status_code, 403)

        # Correct permissions
        Role.objects.create(name='appromanager', bar=self.bar, user=self.user)
        user = User.objects.get(username='nadrieril')
        self.client.force_authenticate(user=user)  # Avoid permission caching
        response = self.client.put('/item/1/?bar=natationjone', data)
        self.assertEqual(response.status_code, 200)


class TransactionPermsTests(APITestCase):
    def setUp(self):
        self.bar = Bar.objects.create(id='natationjone')

        self.user = User.objects.create(username='nadrieril', password='1')
        Role.objects.create(name='customer', bar=self.bar, user=self.user)
        Account.objects.create(bar=self.bar, owner=self.user)

        self.user2 = User.objects.create(username='ntag', password='2')
        Role.objects.create(name='customer', bar=self.bar, user=self.user2)
        Account.objects.create(bar=self.bar, owner=self.user2)

        self.user3 = User.objects.create(username='tizot', password='3')
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
