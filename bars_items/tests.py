from rest_framework.test import APITestCase

from bars_core.models.user import User
from bars_core.models.role import Role
from bars_core.models.bar import Bar
# from bars_base.models.item import Item, ItemDetails

# class ItemTests(APITestCase):
#     def setUp(self):
#         self.bar = Bar.objects.create(id='natationjone')
#         Bar.objects.create(id='avironjone')
#
#         self.user = User.objects.create(username='nadrieril')
#         self.user2 = User.objects.create(username='ntag')
#
#         Role.objects.create(name='appromanager', bar=self.bar, user=self.user2)
#         self.user2 = User.objects.get(username='ntag')
#
#         self.itemdetails = ItemDetails.objects.create(name='Chocolat')
#         self.item = Item.objects.create(details=self.itemdetails, bar=self.bar, price=1)
#         self.create_data = {'details': self.itemdetails.id, 'price': 1}
#         self.update_data = self.client.get('/item/%d/' % self.item.id).data
#         self.update_data['price'] = 4
#
#
#     def test_get_item(self):
#         response = self.client.get('/item/')
#         self.assertEqual(len(response.data), Item.objects.count())
#         self.assertEqual(response.data[0]['price'], self.item.price)
#
#
#     def test_create_item(self):
#         # Unauthenticated
#         response = self.client.post('/item/?bar=natationjone', self.create_data)
#         self.assertEqual(response.status_code, 401)
#
#     def test_create_item1(self):
#         # Wrong permissions
#         self.client.force_authenticate(user=self.user)
#         response = self.client.post('/item/?bar=natationjone', self.create_data)
#         self.assertEqual(response.status_code, 403)
#
#     def test_create_item2(self):
#         # Correct permissions
#         self.client.force_authenticate(user=self.user2)
#         response = self.client.post('/item/?bar=natationjone', self.create_data)
#         self.assertEqual(response.status_code, 201)
#
#     def test_create_item3(self):
#         # Wrong bar
#         self.client.force_authenticate(user=self.user2)
#         response = self.client.post('/item/?bar=avironjone', self.create_data)
#         self.assertEqual(response.status_code, 403)
#
#     def test_create_item4(self):
#         # Non-existing bar
#         self.client.force_authenticate(user=self.user2)
#         response = self.client.post('/item/?bar=rugbyrouje', self.create_data)
#         self.assertEqual(response.status_code, 404)
#
#
#     def test_change_item(self):
#         # Unauthenticated
#         response = self.client.put('/item/%d/?bar=natationjone' % self.item.id, self.update_data)
#         self.assertEqual(response.status_code, 401)
#
#     def test_change_item2(self):
#         # Wrong permissions
#         self.client.force_authenticate(user=self.user)
#         response = self.client.put('/item/%d/?bar=natationjone' % self.item.id, self.update_data)
#         self.assertEqual(response.status_code, 403)
#
#     def test_change_item3(self):
#         # No bar
#         self.client.force_authenticate(user=self.user)
#         response = self.client.put('/item/%d/' % self.item.id, self.update_data)
#         self.assertEqual(response.status_code, 403)
#
#     def test_change_item4(self):
#         # Correct permissions
#         self.client.force_authenticate(user=self.user2)
#         response = self.client.put('/item/%d/?bar=natationjone' % self.item.id, self.update_data)
#         self.assertEqual(response.status_code, 200)
#
#     def test_change_item5(self):
#         # Wrong bar
#         self.client.force_authenticate(user=self.user2)
#         response = self.client.put('/item/%d/?bar=avironjone' % self.item.id, self.update_data)
#         self.assertEqual(response.status_code, 404)
#
#     def test_change_item6(self):
#         # No bar
#         self.client.force_authenticate(user=self.user2)
#         response = self.client.put('/item/%d/' % self.item.id, self.update_data)
#         self.assertEqual(response.status_code, 200)