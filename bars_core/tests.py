from rest_framework.test import APITestCase
from bars_core.models.user import User, UserSerializer

class BackendTests(APITestCase):
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

    def test_login_wrong_password(self):
        data = {'username': 'admin', 'password': 'sdgez'}
        response = self.client.post('/api-token-auth/', data, format='json')

        self.assertEqual(response.status_code, 400)

    def test_login_wrong_user(self):
        data = {'username': 'not_admin', 'password': 'admin'}
        response = self.client.post('/api-token-auth/', data, format='json')

        self.assertEqual(response.status_code, 400)


    def test_add_superuser(self):
        u = User.objects.create_superuser("su", "su")
        self.assertTrue(u.is_superuser)
        self.assertTrue(u.is_staff)



class UserTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user("admin", "admin")
        self.user = User.objects.create_user("bob", "password")
        serializer = UserSerializer(self.user)
        self.data = serializer.data
        self.user_url = '/user/%d/' % self.user.id


    def test_get_user_not_authed(self):
        # Not authenticated
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, 401)

    def test_get_user_authed(self):
        # Authenticated
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, self.data)


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


    def test_change_password(self):
        self.client.force_authenticate(user=self.user)
        self.assertTrue(self.user.check_password('password'))

        data = {'old_password': 'password', 'password': '123456'}
        response = self.client.put('/user/change_password/', data)
        self.assertEqual(response.status_code, 200)

        user_reloaded = User.objects.get(pk=self.user.pk)
        self.assertTrue(user_reloaded.check_password('123456'))

    def test_change_password_wrong_password(self):
        self.client.force_authenticate(user=self.user)
        data = {'old_password': 'wrong_password', 'password': '123456'}
        response = self.client.put('/user/change_password/', data)
        self.assertEqual(response.status_code, 403)
