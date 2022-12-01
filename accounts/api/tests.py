from testing.testcase import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User

# do remember the / at the end, otherwise a redirect response
# would be returned
LOGIN_URL = '/api/accounts/login/'
LOGOUT_URL = '/api/accounts/logout/'
SIGNUP_URL = '/api/accounts/signup/'
LOGIN_STATUS_URL = '/api/accounts/login_status/'


class AccountApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = self.create_user(
            username='Frank',
            email='frank@yahoo.com',
            password='1234567889'
        )

    def test_login(self):
        # login with get method
        response = self.client.get(LOGIN_URL, {
            'username': self.user.username,
            'password': '1234567889'
        })
        self.assertEqual(response.status_code, 405)

        # login with post method but wrong password
        response = self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': '0000000000'
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.post(LOGIN_URL, {
            'username': 'frankly',
            'password': '1234567889'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.data['errors']['user'][0]), 'User does not exist')

        # currently not logged in, test login status
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertFalse(response.data['has_logged_in'])

        # login with post method and correct password
        response = self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': '1234567889'
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['user'], None)
        self.assertEqual(response.data['user']['email'], 'frank@yahoo.com')

        # test current login status
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertTrue(response.data['has_logged_in'])

    def test_logout(self):
        self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': '1234567889'
        })
        # test logout using get method
        response = self.client.get(LOGOUT_URL)
        self.assertEqual(response.status_code, 405)

        # test logout using post method
        response = self.client.post(LOGOUT_URL)
        self.assertEqual(response.status_code, 200)

        # validate logout
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertFalse(response.data['has_logged_in'])

    def test_signup(self):
        # test sign up using get method
        response = self.client.get(SIGNUP_URL, {
            'username': 'testUser',
            'password': 'testpwd',
            'email': 'testemail@email.com'
        })
        self.assertEqual(response.status_code, 405)

        # test sign up with incorrect email addresses format
        response = self.client.post(SIGNUP_URL, {
            'username': 'testUser',
            'password': 'testpwd',
            'email': 'XXXXXXXXXX'
        })
        self.assertEqual(response.status_code, 400)

        # test sign up with short password
        response = self.client.post(SIGNUP_URL, {
            'username': 'testUser',
            'password': 'XX',
            'email': 'testemail@email.com'
        })
        self.assertEqual(response.status_code, 400)

        # test sign up with long username
        response = self.client.post(SIGNUP_URL, {
            'username': 'testUser123456789012345678980',
            'password': 'testpwd',
            'email': 'testemail@email.com'
        })
        self.assertEqual(response.status_code, 400)

        # test successful registration
        response = self.client.post(SIGNUP_URL, {
            'username': 'testUser',
            'password': 'testpwd',
            'email': 'testemail@email.com'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user']['username'], 'testuser')

        # validate login status
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)