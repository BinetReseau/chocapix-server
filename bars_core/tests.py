from rest_framework.test import APITestCase
from bars_core.models.user import User

class BackendTests(APITestCase):
    def setUp(self):
        User.objects.create_user("admin", "admin")

    def test_login(self):
        data = {'password': 'admin', 'username': 'admin'}
        response = self.client.post('/api-token-auth/', data, format='json')

        self.assertEqual(response.status_code, 200)

        token = response.data["token"]
        auth = 'JWT {0}'.format(token)
        response = self.client.get('/user/me/', HTTP_AUTHORIZATION=auth, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], "admin")
