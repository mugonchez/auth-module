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


class TestUserProfile(TestCase):
    def setUp(self):
        # api client
        self.client = APIClient()