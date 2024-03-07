import json
from django.test import TestCase
from authentication.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


class TestUserProfile(TestCase):
    def setUp(self):
        # api client
        self.client = APIClient()
        # urls
        self.login_url = reverse('authentication:login')
        self.profile_url = reverse('authentication:profile')
        # test user
        self.user = User.objects.create_user(
            email = 'john@gmail.com',
            first_name= 'John',
            last_name = 'Doe',
            username = 'Johntez',
            phone_number= '0712345678',
            password = '@Rand0mpassword'
        )

    def test_valid_get_profile_information(self):
        data = {
            'email':'john@gmail.com',
            'password': '@Rand0mpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        access_token = json.loads(response.content)['access']
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.client.get(self.profile_url, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    


    def test_invalid_token_profile_information(self):
        access_token = 'justrandomtoken'
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.client.get(self.profile_url, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    
    def test_valid_update_user_profile_with_put(self):
        data = {
            'email':'john@gmail.com',
            'password': '@Rand0mpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        access_token = json.loads(response.content)['access']
        headers = {'Authorization': f'Bearer {access_token}'}
        data = {
            'first_name': 'John',
            'last_name' :'Doe',
            'username' :'Johntez',
            'phone_number':'0712345678',
        }
        response = self.client.put(self.profile_url, data, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

    def test_invalid_token_update_user_profile_with_put(self):
        access_token = 'somerandomtoken'
        headers = {'Authorization': f'Bearer {access_token}'}
        data = {
            'first_name': 'Jane',
            'last_name': 'Doe'
        }
        response = self.client.put(self.profile_url, data, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    
    def test_invalid_payload_update_user_profile_with_put(self):
        data = {
            'email':'john@gmail.com',
            'password': '@Rand0mpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        access_token = json.loads(response.content)['access']
        headers = {'Authorization': f'Bearer {access_token}'}
        data = {
            'first_name': 'Jane'
        }
        response = self.client.put(self.profile_url, data, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_valid_update_user_profile_with_patch(self):
        data = {
            'email':'john@gmail.com',
            'password': '@Rand0mpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        access_token = json.loads(response.content)['access']
        headers = {'Authorization': f'Bearer {access_token}'}
        data = {
            'first_name': 'Klcare',
        }
        response = self.client.patch(self.profile_url, data, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

    def test_invalid_token_update_user_profile_with_patch(self):
        access_token = 'somerandomtoken'
        headers = {'Authorization': f'Bearer {access_token}'}
        data = {
            'first_name': 'Janes',
        }
        response = self.client.patch(self.profile_url, data, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    
    def test_invalid_payload_update_user_profile_with_patch(self):
        data = {
            'email':'john@gmail.com',
            'password': '@Rand0mpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        access_token = json.loads(response.content)['access']
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.client.patch(self.profile_url, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
