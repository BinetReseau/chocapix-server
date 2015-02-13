from rest_framework.test import APITestCase
from bars_core.models.user import User, UserSerializer

class LoginTests(APITestCase):
    def setUp(self):
        User.objects.create_user("admin", "admin")

    def test_login(self):
        data = {'username': 'admin', 'password': 'admin'}
        response = self.client.post('/api-token-auth/', data, format='json')

        self.assertEqual(response.status_code, 200)

        token = response.data["token"]
        auth = 'JWT {0}'.format(token)
        response = self.client.get('/user/me/', HTTP_AUTHORIZATION=auth, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], "admin")


class UserTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user("admin", "admin")
        self.user = User.objects.create_user("bob", "password")
        serializer = UserSerializer(self.user)
        self.data = serializer.data
        self.user_url = '/user/%d/' % self.user.id


    def test_change_user_not_authed(self):
        # Not authenticated
        self.data['full_name'] = 'alice'
        response = self.client.post(self.user_url, self.data)
        self.assertEqual(response.status_code, 401)

    def test_change_user_self(self):
        # Authenticated as self
        self.data['full_name'] = 'alice'
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.user_url, self.data)
        self.assertEqual(response.status_code, 200)

        response2 = self.client.get(self.user_url)
        self.assertEqual(response2.data['full_name'], self.data['full_name'])
