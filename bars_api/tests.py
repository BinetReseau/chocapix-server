from rest_framework.test import APITestCase

from bars_api.models.user import User
from bars_api.models.role import Role
from bars_api.models.bar import Bar
from bars_api.models.item import Item
from bars_api.models.account import Account


class ItemTests(APITestCase):
    def test_get_item(self):
        response = self.client.get('/item/')
        self.assertEqual(response.data, [])


class ItemPermsTests(APITestCase):
    def setUp(self):
        User.objects.create(username='nadrieril')
        bar = Bar.objects.create(id='natationjone')
        Bar.objects.create(id='avironjone')
        Item.objects.create(name='Chocolat', bar=bar, price=1)

    def test_create_item(self):
        data = {'name': 'test', 'qty': 0, 'bar': 'natationjone', 'price': 1}
        user = User.objects.get(username='nadrieril')
        bar = Bar.objects.get(pk='natationjone')

        # Unauthenticated
        response = self.client.post('/item/?bar=natationjone', data, format='json')
        self.assertEqual(response.status_code, 401)

        # Wrong permissions
        self.client.force_authenticate(user=user)
        response = self.client.post('/item/?bar=natationjone', data, format='json')
        self.assertEqual(response.status_code, 403)

        # Correct permissions
        Role.objects.create(name='appromanager', bar=bar, user=user)
        response = self.client.post('/item/?bar=natationjone', data, format='json')
        self.assertEqual(response.status_code, 201)

        # Wrong bar
        response = self.client.post('/item/?bar=avironjone', data, format='json')
        self.assertEqual(response.status_code, 403)


    def test_change_item(self):
        user = User.objects.get(username='nadrieril')
        bar = Bar.objects.get(pk='natationjone')
        data = self.client.get('/item/1/').data
        data['name'] = "Pizza"

        # Unauthenticated
        response = self.client.put('/item/1/?bar=natationjone', data, format='json')
        self.assertEqual(response.status_code, 401)

        # Wrong permissions
        self.client.force_authenticate(user=user)
        response = self.client.put('/item/1/?bar=natationjone', data, format='json')
        self.assertEqual(response.status_code, 403)

        # Correct permissions
        Role.objects.create(name='appromanager', bar=bar, user=user)
        response = self.client.put('/item/1/?bar=natationjone', data, format='json')
        self.assertEqual(response.status_code, 200)
