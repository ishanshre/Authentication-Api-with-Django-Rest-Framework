"""
Testing the database models
"""


from django.test import TestCase
from django.contrib.auth import get_user_model

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
