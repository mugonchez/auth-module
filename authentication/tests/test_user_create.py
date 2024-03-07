from django.test import TestCase
from authentication.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.core import mail


class TestUserRegistration(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('authentication:register')

    def test_valid_user_registration(self):
        data = {
            'username': 'Johntez',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@gmail.com',
            'phone_number': '0712345678',
            'password': '@Rand0mpassword',
        }
        response = self.client.post(self.register_url, data, format='json')

        # Check if an email was sent
        self.assertEqual(len(mail.outbox), 1)
        
        # Check email subject and recipient
        user_email = mail.outbox[0]
        self.assertEqual(user_email.subject, 'Verify Email To Activate Your Account')
        self.assertEqual(user_email.to, ['john@gmail.com'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='john@gmail.com').exists())
    

    def test_invalid_user_registration(self):
        data = {
            'username': 'Johntez',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@gmail.com',
             'phone_number': '0712345678',
            'password': 'nin' # password does not meet the requirements
        }

        response = self.client.post(self.register_url, data, format='json')

        # Check if an email was sent
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

