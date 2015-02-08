from rest_framework.test import APITestCase

from bars_core.models.user import User
from bars_core.models.role import Role
from bars_core.models.bar import Bar
from bars_base.models.item import Item
from bars_base.models.account import Account


def reload_user(client, user):  # Avoid permission caching
    user = User.objects.get(pk=user.pk)
    client.force_authenticate(user=user)


class ItemTests(APITestCase):
    def setUp(self):
        self.bar = Bar.objects.create(id='natationjone')
        Bar.objects.create(id='avironjone')

        self.user = User.objects.create(username='nadrieril')
        self.user2 = User.objects.create(username='ntag')

        Role.objects.create(name='appromanager', bar=self.bar, user=self.user2)
        self.user2 = User.objects.get(username='ntag')

        self.create_data = {'name': 'test', 'price': 1}
        self.item = Item.objects.create(name='Chocolat', bar=self.bar, price=1)
        self.update_data = self.client.get('/item/1/').data
        self.update_data['name'] = "Pizza"


    def test_get_item(self):
        response = self.client.get('/item/')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.item.name)


    def test_create_item(self):
        # Unauthenticated
        response = self.client.post('/item/?bar=natationjone', self.create_data)
        self.assertEqual(response.status_code, 401)

    def test_create_item1(self):
        # Wrong permissions
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/item/?bar=natationjone', self.create_data)
        self.assertEqual(response.status_code, 403)

    def test_create_item2(self):
        # Correct permissions
        self.client.force_authenticate(user=self.user2)
        response = self.client.post('/item/?bar=natationjone', self.create_data)
        self.assertEqual(response.status_code, 201)

    def test_create_item3(self):
        # Wrong bar
        self.client.force_authenticate(user=self.user2)
        response = self.client.post('/item/?bar=avironjone', self.create_data)
        self.assertEqual(response.status_code, 403)

    def test_create_item4(self):
        # Non-existing bar
        self.client.force_authenticate(user=self.user2)
        response = self.client.post('/item/?bar=rugbyrouje', self.create_data)
        self.assertEqual(response.status_code, 404)


    def test_change_item(self):
        # Unauthenticated
        response = self.client.put('/item/1/?bar=natationjone', self.update_data)
        self.assertEqual(response.status_code, 401)

    def test_change_item2(self):
        # Wrong permissions
        self.client.force_authenticate(user=self.user)
        response = self.client.put('/item/1/?bar=natationjone', self.update_data)
        self.assertEqual(response.status_code, 403)

    def test_change_item3(self):
        # No bar
        self.client.force_authenticate(user=self.user)
        response = self.client.put('/item/1/', self.update_data)
        self.assertEqual(response.status_code, 403)

    def test_change_item4(self):
        # Correct permissions
        self.client.force_authenticate(user=self.user2)
        response = self.client.put('/item/1/?bar=natationjone', self.update_data)
        self.assertEqual(response.status_code, 200)

    def test_change_item5(self):
        # Wrong bar
        self.client.force_authenticate(user=self.user2)
        response = self.client.put('/item/1/?bar=avironjone', self.update_data)
        self.assertEqual(response.status_code, 404)

    def test_change_item6(self):
        # No bar
        self.client.force_authenticate(user=self.user2)
        response = self.client.put('/item/1/', self.update_data)
        self.assertEqual(response.status_code, 200)



class AccountTests(APITestCase):
    def setUp(self):
        self.bar = Bar.objects.create(id='natationjone')
        Bar.objects.create(id='avironjone')

        self.user = User.objects.create(username='nadrieril')
        self.user2 = User.objects.create(username='ntag')

        Role.objects.create(name='admin', bar=self.bar, user=self.user2)
        self.user2 = User.objects.get(username='ntag')

        self.create_data = {'owner': 2}
        self.account = Account.objects.create(owner=self.user, bar=self.bar)
        self.update_data = self.client.get('/account/1/').data
        self.update_data['money'] = 100


    def test_get_account(self):
        response = self.client.get('/account/')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['money'], self.account.money)


    def test_create_account(self):
        # Unauthenticated
        response = self.client.post('/account/?bar=natationjone', self.create_data)
        self.assertEqual(response.status_code, 401)

    def test_create_account1(self):
        # Wrong permissions
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/account/?bar=natationjone', self.create_data)
        self.assertEqual(response.status_code, 403)

    def test_create_account2(self):
        # Correct permissions
        self.client.force_authenticate(user=self.user2)
        response = self.client.post('/account/?bar=natationjone', self.create_data)
        self.assertEqual(response.status_code, 201)

    def test_create_account3(self):
        # Wrong bar
        self.client.force_authenticate(user=self.user2)
        response = self.client.post('/account/?bar=avironjone', self.create_data)
        self.assertEqual(response.status_code, 403)

    def test_create_account4(self):
        # Non-existing bar
        self.client.force_authenticate(user=self.user2)
        response = self.client.post('/account/?bar=rugbyrouje', self.create_data)
        self.assertEqual(response.status_code, 404)


    def test_change_account(self):
        # Unauthenticated
        response = self.client.put('/account/1/?bar=natationjone', self.update_data)
        self.assertEqual(response.status_code, 401)

    def test_change_account2(self):
        # Wrong permissions
        self.client.force_authenticate(user=self.user)
        response = self.client.put('/account/1/?bar=natationjone', self.update_data)
        self.assertEqual(response.status_code, 403)

    def test_change_account3(self):
        # No bar
        self.client.force_authenticate(user=self.user)
        response = self.client.put('/account/1/', self.update_data)
        self.assertEqual(response.status_code, 403)

    def test_change_account4(self):
        # Correct permissions
        self.client.force_authenticate(user=self.user2)
        response = self.client.put('/account/1/?bar=natationjone', self.update_data)
        self.assertEqual(response.status_code, 200)

    def test_change_account5(self):
        # Wrong bar
        self.client.force_authenticate(user=self.user2)
        response = self.client.put('/account/1/?bar=avironjone', self.update_data)
        self.assertEqual(response.status_code, 404)

    def test_change_account6(self):
        # No bar
        self.client.force_authenticate(user=self.user2)
        response = self.client.put('/account/1/', self.update_data)
        self.assertEqual(response.status_code, 200)
