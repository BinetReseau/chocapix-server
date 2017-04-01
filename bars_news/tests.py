from rest_framework.test import APITestCase

from bars_core.models.user import User
from bars_core.models.role import Role
from bars_core.models.bar import Bar
from bars_news.models import News


class NewsTests(APITestCase):
    @classmethod
    def setUpTestData(self):
        super(NewsTests, self).setUpTestData()
        self.bar, _ = Bar.objects.get_or_create(id='natationjone')
        self.bar2, _ = Bar.objects.get_or_create(id='avironjone')

        self.user, _ = User.objects.get_or_create(username='nadrieril')
        self.user2, _ = User.objects.get_or_create(username='ntag')

        Role.objects.get_or_create(name='newsmanager', bar=self.bar, user=self.user2)
        self.user2 = User.objects.get(username='ntag')

        self.create_data = {'name': 'test', 'text': 'example'}
        self.news, _ = News.objects.get_or_create(bar=self.bar, author=self.user, name='', text='')


    def test_get_news(self):
        response = self.client.get('/news/')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.news.name)


    def test_create_news(self):
        # Unauthenticated
        response = self.client.post('/news/?bar=natationjone', self.create_data)
        self.assertEqual(response.status_code, 401)

    def test_create_news1(self):
        # Wrong permissions
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/news/?bar=natationjone', self.create_data)
        self.assertEqual(response.status_code, 403)

    def test_create_news2(self):
        # Correct permissions
        self.client.force_authenticate(user=self.user2)
        response = self.client.post('/news/?bar=natationjone', self.create_data)
        self.assertEqual(response.status_code, 201)

    def test_create_news3(self):
        # Wrong bar
        self.client.force_authenticate(user=self.user2)
        response = self.client.post('/news/?bar=avironjone', self.create_data)
        self.assertEqual(response.status_code, 403)

    def test_create_news4(self):
        # Non-existing bar
        self.client.force_authenticate(user=self.user2)
        response = self.client.post('/news/?bar=rugbyrouje', self.create_data)
        self.assertEqual(response.status_code, 404)
