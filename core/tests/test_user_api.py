"""
Test for user API endpoints
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


User = get_user_model()
CREATE_USER_URL = reverse("accounts:register")


def create_user(**params):
    """Create and return a new user."""
    return User.objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public feature of the User API endpoint"""

    def setUp(self):
        self.client = APIClient()
    
    def test_create_user_success(self):
        """Test creating a user is successfull"""
        payload = {
            "username":"test",
            "email":"test@gmail.com",
            "password":"hello@123",
            "confirm_password":"hello@123",
        }
        # checking if both password mathches
        self.assertEqual(payload['password'],payload['confirm_password'])
        
        # creating user
        res = self.client.post(CREATE_USER_URL, payload)

        # checks if user is successfully created
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email=payload['email'])

        # check if the password is correct
        self.assertTrue(user.check_password(payload['password']))

        # check that password or its hash is not in the res.data. 
        self.assertNotIn("password",res.data)
    
    def test_user_with_email_exists_error(self):
        """Test error returned if user with email already exists"""
        payload = {
            "username":"test",
            "email":"test@gmail.com",
            "password":"hello@123",
        }
        payload1 = {
            "username":"test",
            "email":"test@gmail.com",
            "password":"hello@123",
            "confirm_password":"hello@123",
        }
        self.assertEqual(payload["email"], payload1['email'])
        self.assertEqual(payload["username"], payload1['username'])
        self.assertEqual(payload["password"], payload1['password'])
        self.assertEqual(payload["password"], payload1['confirm_password'])

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload1)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        

    def test_user_with_username_exists(self):
        """Test error returned if user with username already exists"""
        payload = {
            "username":"test",
            "email":"test123@gmail.com",
            "password":"hello@123",
        }
        payload1 = {
            "username":"test",
            "email":"test123@gmail.com",
            "password":"hello@123",
            "confirm_password":"hello@123",
        }
        self.assertEqual(payload["email"], payload1['email'])
        self.assertEqual(payload["username"], payload1['username'])
        self.assertEqual(payload["password"], payload1['password'])
        self.assertEqual(payload["password"], payload1['confirm_password'])

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload1)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_password_too_short_error(self):
        """Test error returned if passord is less than 8 characters"""
        payload = {
            "username":"test",
            "email":"test123@gmail.com",
            "password":"hello",
            "confirm_password":"hello",
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = User.objects.filter(username=payload['username'])
        self.assertFalse(user_exists)