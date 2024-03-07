import json
from django.test import TestCase
from authentication.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


class TestUserRefreshToken(TestCase):
    def setUp(self):
        # api client
        self.client = APIClient()
        # urls
        self.refresh_url = reverse('authentication:refresh')
        self.login_url = reverse('authentication:login')

        # test user
        self.user = User.objects.create_user(
            email = 'john@gmail.com',
            first_name= 'John',
            last_name = 'Doe',
            username = 'Johntez',
            phone_number= '0712345678',
            password = '@Rand0mpassword'
        )
    
    def test_valid_refresh_token(self): 
        data = {
            'email':'john@gmail.com',
            'password': '@Rand0mpassword'
        }
        # login user to get the access and refresh token
        response = self.client.post(self.login_url, data, format='json')
        refresh_token = json.loads(response.content)['refresh']
        data = {
            "refresh": refresh_token
        }
        response = self.client.post(self.refresh_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

    def test_invalid_refresh_token(self):
        refresh_token = "justsomerandomcharacters" # invalid refresh token
        data = {
            "refresh": refresh_token
        }
        response = self.client.post(self.refresh_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


