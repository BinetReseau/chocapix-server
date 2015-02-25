from rest_framework.test import APITestCase

from bars_core.models.user import User
from bars_core.models.role import Role
from bars_core.models.bar import Bar
# from bars_base.models.item import Item, ItemDetails
from bars_core.models.account import Account
from bars_transactions.models import Transaction


# class TransactionTests(APITestCase):
#     def setUp(self):
#         self.bar, _ = Bar.objects.get_or_create(id='natationjone')
#         self.bar2, _ = Bar.objects.get_or_create(id='natationrouge')
#
#         self.user, _ = User.objects.get_or_create(username='nadrieril')
#         Account.objects.get_or_create(bar=self.bar, owner=self.user)
#
#         self.user2, _ = User.objects.get_or_create(username='ntag')
#         Account.objects.get_or_create(bar=self.bar, owner=self.user2)
#
#         self.user3, _ = User.objects.get_or_create(username='tizot')
#         Role.objects.get_or_create(name='staff', bar=self.bar, user=self.user3)
#         Account.objects.get_or_create(bar=self.bar, owner=self.user3)
#
#         self.user4, _ = User.objects.get_or_create(username='marioyc')
#         Role.objects.get_or_create(name='staff', bar=self.bar2, user=self.user4)
#         Account.objects.get_or_create(bar=self.bar2, owner=self.user4)
#
#         itemdetails, _ = ItemDetails.objects.get_or_create(name='Chocolat')
#         self.item, _ = Item.objects.get_or_create(details=itemdetails, bar=self.bar, price=1)
#
#         Transaction.objects.get_or_create(bar=self.bar, author=self.user)
#
#         Transaction.objects.get_or_create(bar=self.bar2, author=self.user4)
#
#
#     def test_cancel_transaction(self):
#         self.client.force_authenticate(user=self.user)
#         response = self.client.put('/transaction/1/cancel/', {})
#         self.assertEqual(response.status_code, 200)
#         transaction = Transaction.objects.get(pk=1)
#         self.assertTrue(transaction.canceled)
#
#     def test_cancel_unexisting_transaction(self):
#         self.client.force_authenticate(user=self.user)
#         response = self.client.put('/transaction/3/cancel/', {})
#         self.assertEqual(response.status_code, 404)
#
#     def test_restore_transaction(self):
#         self.client.force_authenticate(user=self.user)
#         response = self.client.put('/transaction/1/restore/', {})
#         self.assertEqual(response.status_code, 200)
#         transaction = Transaction.objects.get(pk=1)
#         self.assertFalse(transaction.canceled)
#
#     def test_cancel_transaction_wrong_user(self):
#         self.client.force_authenticate(user=self.user2)
#         response = self.client.put('/transaction/1/cancel/', {})
#         self.assertEqual(response.status_code, 403)
#         transaction = Transaction.objects.get(pk=1)
#         self.assertFalse(transaction.canceled)
#
#     def test_cancel_transaction_staff(self):
#         self.client.force_authenticate(user=self.user3)
#         response = self.client.put('/transaction/1/cancel/', {})
#         self.assertEqual(response.status_code, 200)
#         transaction = Transaction.objects.get(pk=1)
#         self.assertTrue(transaction.canceled)
#
#     def test_cancel_transaction_staff_wrong_bar(self):
#         self.client.force_authenticate(user=self.user3)
#         response = self.client.put('/transaction/2/cancel/', {})
#         self.assertEqual(response.status_code, 403)
#         transaction = Transaction.objects.get(pk=2)
#         self.assertFalse(transaction.canceled)
#
#     def test_cancel_transaction_two_bars(self):
#         Role.objects.get_or_create(name='staff', bar=self.bar, user=self.user4)
#         Account.objects.get_or_create(bar=self.bar, owner=self.user4)
#         self.client.force_authenticate(user=self.user4)
#
#         response = self.client.put('/transaction/1/cancel/', {})
#         self.assertEqual(response.status_code, 200)
#         transaction = Transaction.objects.get(pk=1)
#         self.assertTrue(transaction.canceled)
#
#         response2 = self.client.put('/transaction/2/cancel/', {})
#         self.assertEqual(response2.status_code, 200)
#         transaction2 = Transaction.objects.get(pk=2)
#         self.assertTrue(transaction2.canceled)
#
#     # TODO: move to operation tests
#     def test_create_cancel_buytransaction(self):
#         data = {'type':'buy', 'item':self.item.id, 'qty':1}
#         start_qty = Item.objects.get(id=self.item.id).qty
#
#         self.client.force_authenticate(user=self.user)
#
#         response = self.client.post('/transaction/?bar=natationjone', data)
#         self.assertEqual(response.status_code, 201)
#         end_qty = Item.objects.get(id=self.item.id).qty
#         self.assertEqual(end_qty, start_qty - 1)
#
#         response2 = self.client.put('/transaction/3/cancel/', {})
#         self.assertEqual(response2.status_code, 200)
#         end_qty = Item.objects.get(id=self.item.id).qty
#         self.assertEqual(end_qty, start_qty)
#
#         response3 = self.client.put('/transaction/3/cancel/', {})
#         self.assertEqual(response3.status_code, 200)
#         end_qty = Item.objects.get(id=self.item.id).qty
#         self.assertEqual(end_qty, start_qty)
