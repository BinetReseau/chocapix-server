from django.test import TestCase
from rest_framework.test import APIClient
from django.test.utils import override_settings

class BackendTests(TestCase):
    def setUp(self):
        from bars_api.models.user import User
        User.objects.create_user("admin", "admin")

    def test_authentication(self):
        from django.contrib.auth import authenticate
        user = authenticate(password="admin")
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "admin")

    def test_login(self):
        client = APIClient(enforce_csrf_checks=True)
        data = {'password':"admin"}
        response = client.post('/api-token-auth/', data, format='json')

        self.assertEqual(response.status_code, 200)

        token = response.data["token"]
        auth = 'JWT {0}'.format(token)
        response = client.get('/user/me/', HTTP_AUTHORIZATION=auth, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], "admin")
