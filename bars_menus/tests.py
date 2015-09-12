# coding: utf-8 

from rest_framework.test import APITestCase

from bars_core.models.user import User
from bars_core.models.role import Role
from bars_core.models.bar import Bar
from bars_core.models.account import Account
from bars_items.models.sellitem import SellItem
from bars_menus.models import Menu, MenuSellItem


class MenuTests(APITestCase):
    @classmethod
    def setUpTestData(self):
        super(MenuTests, self).setUpTestData()

        self.bar1, _ = Bar.objects.get_or_create(id='avironjone')
        self.bar2, _ = Bar.objects.get_or_create(id='natationjone')

        self.user1, _ = User.objects.get_or_create(username='ntag')
        self.user2, _ = User.objects.get_or_create(username='tizot')
        self.user3, _ = User.objects.get_or_create(username='nadrieril')

        Role.objects.get_or_create(name='customer', bar=self.bar1, user=self.user1)
        Role.objects.get_or_create(name='customer', bar=self.bar1, user=self.user2)
        Role.objects.get_or_create(name='customer', bar=self.bar2, user=self.user3)
        self.user1 = User.objects.get(username='ntag')
        self.user2 = User.objects.get(username='tizot')
        self.user3 = User.objects.get(username='nadrieril')

        self.account1, _ = Account.objects.get_or_create(owner=self.user1, bar=self.bar1)
        self.account2, _ = Account.objects.get_or_create(owner=self.user2, bar=self.bar1)
        self.account3, _ = Account.objects.get_or_create(owner=self.user3, bar=self.bar2)

        self.sellitem1, _ = SellItem.objects.get_or_create(bar=self.bar1, name="Chocolat", tax=0.2)
        self.sellitem2, _ = SellItem.objects.get_or_create(bar=self.bar1, name="Nutella", tax=0.2)

        self.create_data = {'name': 'Petit dejeuner', 'items': [{'sellitem': self.sellitem1.id, 'qty': 10}, {'sellitem': self.sellitem2.id, 'qty': 5}]} 
        self.menu, _ = Menu.objects.get_or_create(account=self.account1, name='Gouter')
        self.menu_sellitem, _ = MenuSellItem.objects.get_or_create(menu=self.menu, sellitem=self.sellitem1, qty=2)

    def test_get_menu(self):
        response = self.client.get('/menu/')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.menu.name)

    def test_create_menu_1(self):
        # Unauthenticated
        response = self.client.post('/menu/?bar=avironjone', self.create_data)
        self.assertEqual(response.status_code, 401)

    def test_create_menu_2(self):
        # Correct permissions
        self.client.force_authenticate(user=self.user1)
        self.create_data['account'] = self.account1.id
        response = self.client.post('/menu/?bar=avironjone', self.create_data)
        self.assertEqual(response.status_code, 201)

    def test_create_menu_3(self):
        # Wrong bar
        self.client.force_authenticate(user=self.user3)
        response = self.client.post('/menu/?bar=avironjone', self.create_data)
        self.assertEqual(response.status_code, 403)

    def test_create_menu_4(self):
        # Non-existing bar
        self.client.force_authenticate(user=self.user2)
        response = self.client.post('/menu/?bar=rugbyrouje', self.create_data)
        self.assertEqual(response.status_code, 404)

    def test_delete_menu_1(self):
        # Wrong permissions (wrong account)
        self.client.force_authenticate(user=self.user2)
        menu_id = self.client.get('/menu/').data[0]['id']
        response = self.client.delete('/menu/%d/?bar=avironjone' % menu_id)
        self.assertEqual(response.status_code, 403)

    def test_delete_menu_2(self):
        # Wrong permissions (wrong bar)
        self.client.force_authenticate(user=self.user3)
        menu_id = self.client.get('/menu/').data[0]['id']
        response = self.client.delete('/menu/%d/?bar=avironjone' % menu_id)
        self.assertEqual(response.status_code, 403)

    # def test_delete_menu_3(self):
    #     # Correct permissions
    #     self.client.force_authenticate(user=self.user1)
    #     menu_id = self.client.get('/menu/').data[0]['id']
    #     response = self.client.delete('/menu/%d/?bar=avironjone' % menu_id)
    #     self.assertEqual(response.status_code, 200)

    # Tests for change_menu
