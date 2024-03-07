import json
from django.test import TestCase
from authentication.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from authentication.utils import generate_token
from django.core import mail
from django.conf import settings


class TestUserChangePassword(TestCase):
    def setUp(self):
        # api client
        self.client = APIClient()
        #urls
        self.login_url = reverse('authentication:login')
        self.change_password_url = reverse('authentication:change-password')
        # test user
        self.user = User.objects.create_user(
            email = 'john@gmail.com',
            first_name= 'John',
            last_name = 'Doe',
            username = 'Johntez',
            phone_number= '0712345678',
            password = '@Rand0mpassword'
        )


    def test_valid_change_password(self):
        data = {
            'email':'john@gmail.com',
            'password': '@Rand0mpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        access_token = json.loads(response.content)['access']
        headers = {'Authorization': f'Bearer {access_token}'}
        current_user_password = '@Rand0mpassword'
        new_password = 's0mew3rdP@ss'
        data = {
            'current_password': current_user_password,
            'new_password': new_password
        }
        response = self.client.post(self.change_password_url, data, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    

    def test_unauthorized_change_password(self):
        current_user_password = '@Rand0mpassword'
        new_password = 's0mew3rdP@ss'
        data = {
            'current_password': current_user_password,
            'new_password': new_password
        }
        response = self.client.post(self.change_password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



    def test_invalid_change_password(self):
        data = {
            'email':'john@gmail.com',
            'password': '@Rand0mpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        access_token = json.loads(response.content)['access']
        headers = {'Authorization': f'Bearer {access_token}'}
        current_user_password = 'wrongpassword' # current wrong password
        new_password = 's0mew3rdP@ss'
        data = {
            'current_password': current_user_password,
            'new_password': new_password
        }
        response = self.client.post(self.change_password_url, data, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
