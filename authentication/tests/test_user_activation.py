from django.test import TestCase
from authentication.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from authentication.utils import generate_token


class TestUserActivation(TestCase):
    def setUp(self):
        # api client
        self.client = APIClient()
        #urls
        self.activate_url = reverse('authentication:activate')
        # test user
        self.user = User.objects.create_user(
            email = 'john@gmail.com',
            first_name= 'John',
            last_name = 'Doe',
            username = 'Johntez',
            phone_number= '0712345678',
            password = '@Rand0mpassword'
        )

        # update user is active state
        self.user.is_active = False
        self.user.save()
        

    
    def test_valid_account_activation(self):
        # encode the user id and generate token
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = generate_token(self.user)

        data = {
            "uid": uid,
            "token": token
        }
        response = self.client.post(self.activate_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(User.objects.get(email=self.user.email).is_active)


    def test_invalid_account_activation(self):
        data = {
            "uid": "randomuid", # invalid uid
            "token": "randomtoken" # invalid token
        }
        response = self.client.post(self.activate_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.get(email=self.user.email).is_active)








