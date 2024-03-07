from django.test import TestCase
from authentication.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.core import mail



class TestUserResendActivation(TestCase):
    def setUp(self):
        # api client
        self.client = APIClient()
        #urls
        self.resend_activation_url = reverse('authentication:resend-activation')
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

    def test_valid_resend_activation(self):
        email = self.user.email
        data = {
            'email': email
        }
        response = self.client.post(self.resend_activation_url, data, format='json')
        # Check if an email was sent
        self.assertEqual(len(mail.outbox), 1)
        # Check email subject and recipient
        user_email = mail.outbox[0]
        self.assertEqual(user_email.subject, 'Verify Email To Activate Your Account')
        self.assertEqual(user_email.to, [email])
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    

    def test_invalid_resend_activation(self):
        email = 'justrandomemail@gmail.com' # non-existent email
        data = {
            'email': email
        }
        response = self.client.post(self.resend_activation_url, data, format='json')
        # Check if an email was sent
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)




