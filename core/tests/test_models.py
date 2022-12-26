"""
Testing the database models
"""


from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.models import Profile

User = get_user_model()


class ModelTests(TestCase):
    """Test Models"""
    def test_create_user(self):
        """Testing creating a user"""
        email = "test123@email.com"
        username = "test123"
        password = "testingPass123"
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)


    def test_create_superuser(self):
        """Test to create a super user"""
        email = "test1@email.com"
        username = "test123"
        password = "testPassword"
        user = User.objects.create_superuser(
            email=email,
            username=username,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
    
    def test_create_user_has_email_not_verified(self):
        """Testing new user has email not verified"""
        email = "test1@gmail.com"
        password = "testPass"
        username = "hello"
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.email_confirmed)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_create_superuser_has_email_not_verified(self,):
        """Test new super user has no email verified"""
        email = "test1@email.com"
        username = "test123"
        password = "testPassword"
        user = User.objects.create_superuser(
            email=email,
            username=username,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.email_confirmed)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
    
    def test_user_created_with_no_username_raises_value_error(self):
        """Test create new user with no username or blank username raises Value error"""
        email = "test@email.com"
        password = "helllooo"
        with self.assertRaises(ValueError):
            User.objects.create_user(
                username="",
                email=email,
                password=password,
            )
    def test_user_created_has_its_own_profile(self):
        """Test new user has its own profile created"""
        email = "test@email.com"
        password = "helllooo"
        username = "test"
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        profile = Profile.objects.get(user=user)
        self.assertEqual(user.id, profile.user.id)

        