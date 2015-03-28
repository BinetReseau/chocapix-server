from datetime import timedelta
from django.utils import timezone
from rest_framework.test import APITestCase

from bars_core.models.bar import Bar
from bars_core.models.user import User
from bars_core.models.role import Role
from bars_core.models.account import Account

from bars_items.models.buyitem import BuyItem
from bars_items.models.itemdetails import ItemDetails
from bars_items.models.sellitem import SellItem
from bars_items.models.stockitem import StockItem

from bars_transactions.models import Transaction


def reload(obj):
    return obj.__class__.objects.get(pk=obj.pk)

class TransactionTests(APITestCase):
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

        self.staff_user, _ = User.objects.get_or_create(username='staff_user')
        self.staff_account, _ = Account.objects.get_or_create(bar=self.bar, owner=self.staff_user)
        self.staff_role, _ = Role.objects.get_or_create(name='staff', bar=self.bar, user=self.staff_user)

        self.sellitem, _ = SellItem.objects.get_or_create(bar=self.bar, name="Chocolat", tax=0.2)
        self.itemdetails, _ = ItemDetails.objects.get_or_create(name="Chocolat")
        self.buyitem, _ = BuyItem.objects.get_or_create(details=self.itemdetails, itemqty=2.5)
        self.stockitem, _ = StockItem.objects.get_or_create(bar=self.bar, sellitem=self.sellitem, details=self.itemdetails, price=1)
        self.stockitem.unit_factor = 5
        self.stockitem.qty = 5
        self.stockitem.save()

        self.transaction = Transaction.objects.create(bar=self.bar, author=self.user)
        self.transaction_url = '/transaction/%d/' % self.transaction.id


    def setUp(self):
        self.transaction.canceled = False
        self.transaction.save()
        self.user = reload(self.user)
        self.staff_user = reload(self.staff_user)

    def test_cancel_transaction(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put(self.transaction_url + 'cancel/', {})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(reload(self.transaction).canceled)

    def test_restore_transaction(self):
        self.transaction.canceled = True
        self.transaction.save()
        self.client.force_authenticate(user=self.user)

        response = self.client.put(self.transaction_url + 'restore/', {})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(reload(self.transaction).canceled)

    def test_cancel_transaction_wrong_user(self):
        self.client.force_authenticate(user=self.wrong_user)

        response = self.client.put(self.transaction_url + 'cancel/', {})
        self.assertEqual(response.status_code, 403)
        self.assertFalse(reload(self.transaction).canceled)

    def test_cancel_transaction_staff(self):
        self.client.force_authenticate(user=self.staff_user)

        response = self.client.put(self.transaction_url + 'cancel/', {})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(reload(self.transaction).canceled)

    def test_cancel_transaction_staff_wrong_bar(self):
        self.client.force_authenticate(user=self.staff_user)
        transaction = Transaction.objects.create(bar=self.wrong_bar, author=self.wrong_user)

        response = self.client.put('/transaction/%d/cancel/' % transaction.id, {})
        self.assertEqual(response.status_code, 403)
        self.assertFalse(reload(transaction).canceled)

    # TODO: move to operation tests
    def test_create_cancel_buytransaction(self):
        data = {'type':'buy', 'stockitem':self.stockitem.id, 'qty':1}
        start_qty = reload(self.stockitem).qty

        self.client.force_authenticate(user=self.user)

        response = self.client.post('/transaction/?bar=%s' % self.bar.id, data)
        self.assertEqual(response.status_code, 201)
        end_qty = reload(self.stockitem).qty
        self.assertEqual(end_qty, start_qty - 1. / self.stockitem.get_unit('sell'))
        transaction_id = response.data['id']

        response2 = self.client.put('/transaction/%d/cancel/' % transaction_id, {})
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(reload(self.stockitem).qty, start_qty)

        response3 = self.client.put('/transaction/%d/cancel/' % transaction_id, {})
        self.assertEqual(response3.status_code, 200)
        self.assertEqual(reload(self.stockitem).qty, start_qty)

        response4 = self.client.put('/transaction/%d/restore/' % transaction_id, {})
        self.assertEqual(response4.status_code, 200)
        self.assertEqual(reload(self.stockitem).qty, end_qty)


    def test_cancel_transaction_after_threshold(self):
        self.bar.cancel_transaction_threshold = 48
        self.bar.save()
        transaction = Transaction.objects.create(bar=self.bar, author=self.user)
        transaction.timestamp = timezone.now() - timedelta(hours=49)
        transaction.save()

        self.client.force_authenticate(user=self.user)
        response = self.client.put('/transaction/%d/cancel/' % transaction.id, {})
        self.assertEqual(response.status_code, 403)
        self.assertFalse(reload(transaction).canceled)

        self.client.force_authenticate(user=self.staff_user)
        response = self.client.put('/transaction/%d/cancel/' % transaction.id, {})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(reload(transaction).canceled)
