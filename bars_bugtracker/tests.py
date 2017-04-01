from mock import Mock, patch
from rest_framework.test import APITestCase

from bars_core.models.user import User
from bars_core.models.bar import Bar
from bars_bugtracker.models import BugReport


def reload(obj):
    return obj.__class__.objects.get(pk=obj.pk)

class BugreportTests(APITestCase):
    @classmethod
    def setUpClass(self):
        super(BugreportTests, self).setUpClass()
        self.bar, _ = Bar.objects.get_or_create(id='natationjone')
        self.user, _ = User.objects.get_or_create(username='bob')

        self.create_data = {'message': 'test', 'data': 'error'}


    def test_create_bugreport(self):
        # Unauthenticated
        response = self.client.post('/bugreport/?bar=natationjone', self.create_data)
        self.assertEqual(response.status_code, 401)

    def test_create_bugreport1(self):
        # Wrong permissions
        with patch.object(User, 'has_perm', return_value=False):
            self.client.force_authenticate(user=self.user)
            response = self.client.post('/bugreport/?bar=natationjone', self.create_data)
            self.assertEqual(response.status_code, 403)

    def test_create_bugreport2(self):
        # Correct permissions
        with patch.object(User, 'has_perm', return_value=True) as m:
            self.client.force_authenticate(user=self.user)
            response = self.client.post('/bugreport/?bar=natationjone', self.create_data)
            self.assertEqual(response.status_code, 201)

        self.assertEqual(m.call_args[0][0], 'bars_bugtracker.add_bugreport')
        bugreport = BugReport.objects.get(id=response.data.get('id'))
        self.assertEqual(bugreport.bar, self.bar)
        self.assertEqual(bugreport.author, self.user)
        self.assertEqual(bugreport.message, self.create_data.get('message'))
