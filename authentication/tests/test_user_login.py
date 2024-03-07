from django.test import TestCase
from authentication.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


class TestUserLogin(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('authentication:login')

        self.user = User.objects.create_user(
            email = 'john@gmail.com',
            first_name= 'John',
            last_name = 'Doe',
            username = 'Johntez',
            phone_number= '0712345678',
            password = '@Rand0mpassword'
        )

    
    def test_valid_user_login(self):
        data = {
            'email':'john@gmail.com',
            'password': '@Rand0mpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

    def test_invalid_user_login(self):
        data = {
            'email':'john@gmail.com',
            'password': 'wrongpassword' # validate wrong password
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)





    


