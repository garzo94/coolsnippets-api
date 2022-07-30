from wsgiref import headers
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

# import models
# Create your tests here.



def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)
############### user MOdel################
class UserModelTest(TestCase):
    ###Test model user ####
    def test_create_user_successfuly(self):
        email = 'user1@example.com'
        username = 'myusername'

        user = get_user_model().objects.create_user(
            email=email,
            username=username,

        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
        # self.assertEqual(user.password, password)

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        i=1

        for email, expected in sample_emails:
            i += 2
            user = get_user_model().objects.create_user(
            email=email,
            username=f"holapapu{i}",

        )
            self.assertEqual(user.email, expected)



class PublicUserApiTests(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            'username': 'TestName',
            'email': 'test@example.com',
            'password': 'testpass123',

        }
        res = self.client.post('/api/auth/users/', payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password'])) #if the user was created succesfully this check  if the password is correct
        self.assertNotIn('password', res.data) # check if the key passowrd is not in the data

    def test_user_with_email_username_exists_error(self):
            """Test error returned if user with email exists."""
            payload = {
                'username': 'TestName45',
                'email': 'test@example.com',
                'password': 'testpass123',

            }
            create_user(**payload)
            res = self.client.post('/api/auth/users/', payload)

            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_logout_succesully(self):
        payload = {
                'username': 'TestName45',
                'email': 'test@example.com',
                'password': 'testpass123',

            }
        create_user(**payload)


        res = self.client.post('/api/auth/token/login/', {'username': 'TestName45','password': 'testpass123',})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('auth_token', res.data)#

        token = 'Token '+res.data.get('auth_token')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        resLogout = self.client.post('/api/auth/token/logout/')
        self.assertEqual(resLogout.status_code, status.HTTP_204_NO_CONTENT)
    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid."""
        create_user(username='myusername',email='test@example.com', password='goodpass')

        payload = {'email': 'test@example.com', 'password': 'badpass'}
        res = self.client.post('/api/auth/token/login/', payload)

        self.assertNotIn('auth_token', res.data)# we are making suer that the token is not created with bad credentials
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error."""
        payload = {'username':'holaquepdo','email': 'test@example.com', 'password': ''}
        res = self.client.post('/api/auth/token/login/', payload)

        self.assertNotIn('auth_token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test authentication is required for users."""


        res = self.client.get('http://localhost:8000/api/auth/users/me',{}, True)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)






