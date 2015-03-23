from rest_framework.test import APITestCase
from bars_django.utils import get_root_bar
from bars_core.models.bar import Bar, BarSerializer
from bars_core.models.user import User, UserSerializer
from bars_core.models.role import Role
from bars_core.models.account import Account, AccountSerializer


def reload(obj):
    return obj.__class__.objects.get(pk=obj.pk)


class BackendTests(APITestCase):
    @classmethod
    def setUpClass(self):
        User.objects.create_user("test", "test")


    def test_login(self):
        data = {'username': 'test', 'password': 'test'}
        response = self.client.post('/api-token-auth/', data, format='json')

        self.assertEqual(response.status_code, 200)

        token = response.data["token"]
        auth = 'JWT {0}'.format(token)
        response = self.client.get('/user/me/', HTTP_AUTHORIZATION=auth, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], "test")

    def test_login_wrong_password(self):
        data = {'username': 'test', 'password': 'sdgez'}
        response = self.client.post('/api-token-auth/', data, format='json')

        self.assertEqual(response.status_code, 400)

    def test_login_wrong_user(self):
        data = {'username': 'not_admin', 'password': 'test'}
        response = self.client.post('/api-token-auth/', data, format='json')

        self.assertEqual(response.status_code, 400)


    def test_add_superuser(self):
        u = User.objects.create_superuser("su", "su")
        self.assertTrue(u.is_superuser)
        self.assertTrue(u.is_staff)



class BarTests(APITestCase):
    @classmethod
    def setUpClass(self):
        get_root_bar._cache = None  # Workaround
        root_bar = get_root_bar()
        self.admin, _ = User.objects.get_or_create(username="admin")
        Role.objects.get_or_create(bar=root_bar, user=self.admin, name="admin")
        self.admin = reload(self.admin)  # prevent role caching

        self.bar, _ = Bar.objects.get_or_create(id="barrouje")

        serializer = BarSerializer(self.bar)
        self.data = serializer.data
        del self.data['next_scheduled_appro']
        self.data['name'] = "barjone"
        self.bar_url = '/bar/%s/' % self.bar.id

    def setUp(self):
        self.bar.name = "barrouje"
        self.bar.save()


    def test_get_bar_not_authed(self):
        # Not authenticated
        response = self.client.get(self.bar_url)
        self.assertEqual(response.status_code, 200)

    def test_get_bar_authed(self):
        # Authenticated
        self.client.force_authenticate(user=User())
        response = self.client.get(self.bar_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.bar.name)


    def test_change_bar_no_perms(self):
        # Not authenticated
        self.client.force_authenticate(user=User())
        response = self.client.put(self.bar_url, self.data)
        self.assertEqual(response.status_code, 403)

    def test_change_bar_admin(self):
        # Authenticated as admin
        self.client.force_authenticate(user=self.admin)
        response = self.client.put(self.bar_url, self.data)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(reload(self.bar).name, self.data['name'])


class UserTests(APITestCase):
    @classmethod
    def setUpClass(self):
        get_root_bar._cache = None  # Workaround
        root_bar = get_root_bar()
        self.admin, _ = User.objects.get_or_create(username="admin")
        Role.objects.get_or_create(bar=root_bar, user=self.admin, name="admin")
        self.admin = reload(self.admin)  # prevent role caching

        self.user, _ = User.objects.get_or_create(username="bob")
        self.user.set_password("password")
        self.user.save()

        serializer = UserSerializer(self.user)
        self.data = serializer.data
        self.user_url = '/user/%d/' % self.user.id

    def setUp(self):
        self.data['username'] = "bob"
        self.user.username = "bob"
        self.user.save()


    def test_get_user_not_authed(self):
        # Not authenticated
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, 401)

    def test_get_user_authed(self):
        # Authenticated
        self.client.force_authenticate(user=User())
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], self.data['username'])


    def test_change_user_no_perms(self):
        # Not authenticated
        self.client.force_authenticate(user=User())
        self.data['username'] = 'alice'
        response = self.client.put(self.user_url, self.data)
        self.assertEqual(response.status_code, 403)

    def test_change_user_admin(self):
        # Authenticated as admin
        self.data['username'] = 'alice'
        self.client.force_authenticate(user=self.admin)
        response = self.client.put(self.user_url, self.data)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(reload(self.user).username, self.data['username'])

    def test_change_user_self(self):
        # Authenticated as self
        self.data['username'] = 'alice'
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.user_url, self.data)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(reload(self.user).username, self.data['username'])


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


class AccountTests(APITestCase):
    @classmethod
    def setUpClass(self):
        self.bar, _ = Bar.objects.get_or_create(id='natationjone')
        Bar.objects.get_or_create(id='avironjone')

        self.user, _ = User.objects.get_or_create(username='nadrieril')
        self.user2, _ = User.objects.get_or_create(username='ntag')

        Role.objects.get_or_create(name='admin', bar=self.bar, user=self.user2)
        self.user2 = User.objects.get(username='ntag')

        self.create_data = {'owner': self.user2.id}
        self.account, _ = Account.objects.get_or_create(owner=self.user, bar=self.bar)
        self.update_data = AccountSerializer(self.account).data
        self.update_data['deleted'] = True

    def setUp(self):
        self.account.deleted = False
        self.account.save()


    def test_get_account(self):
        response = self.client.get('/account/')
        self.assertEqual(len(response.data), Account.objects.all().count())
        self.assertEqual(response.data[0]['deleted'], self.account.deleted)


    def test_create_account(self):
        # Unauthenticated
        response = self.client.post('/account/?bar=natationjone', self.create_data)
        self.assertEqual(response.status_code, 401)

    def test_create_account1(self):
        # Wrong permissions
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/account/?bar=natationjone', self.create_data)
        self.assertEqual(response.status_code, 403)

    def test_create_account2(self):
        # Correct permissions
        self.client.force_authenticate(user=self.user2)
        response = self.client.post('/account/?bar=natationjone', self.create_data)
        self.assertEqual(response.status_code, 201)

    def test_create_account3(self):
        # Wrong bar
        self.client.force_authenticate(user=self.user2)
        response = self.client.post('/account/?bar=avironjone', self.create_data)
        self.assertEqual(response.status_code, 403)

    def test_create_account4(self):
        # Non-existing bar
        self.client.force_authenticate(user=self.user2)
        response = self.client.post('/account/?bar=rugbyrouje', self.create_data)
        self.assertEqual(response.status_code, 404)


    def test_change_account(self):
        # Unauthenticated
        response = self.client.put('/account/%d/?bar=natationjone' % self.account.id, self.update_data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(reload(self.account).deleted, self.account.deleted)

    def test_change_account2(self):
        # Wrong permissions
        self.client.force_authenticate(user=self.user)
        response = self.client.put('/account/%d/?bar=natationjone' % self.account.id, self.update_data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(reload(self.account).deleted, self.account.deleted)

    def test_change_account4(self):
        # Correct permissions
        self.client.force_authenticate(user=self.user2)
        response = self.client.put('/account/%d/?bar=natationjone' % self.account.id, self.update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(reload(self.account).deleted, self.update_data['deleted'])

    def test_change_account5(self):
        # Wrong bar
        self.client.force_authenticate(user=self.user2)
        response = self.client.put('/account/%d/?bar=avironjone' % self.account.id, self.update_data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(reload(self.account).deleted, self.account.deleted)
