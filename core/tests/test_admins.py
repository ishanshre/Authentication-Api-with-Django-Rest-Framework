"""
Test Django Admin Pannel
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class AdminSiteTest(TestCase):
    """Test django admin"""
    def setUp(self):
        """
        The codes in this method is going to be run before every single test runs that we add to this class
        Create admin user and client
        """
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            email="admin123@admin.com",
            username="admin123",
            password="test@123",
        )
        #force login method to authenticate django admin with superuser
        self.client.force_login(self.admin_user)
        self.user = User.objects.create_user(
            email="user@email.com",
            username="user",
            password="test@123",
        )
    
    def test_user_list_works(self):
        """Testing list of user works or not"""
        url = reverse("admin:accounts_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.username)
        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.is_staff)
        self.assertContains(res, self.user.email_confirmed)
    
    def test_user_edit_works(self):
        """Test the user edit and detial page works"""
        url = reverse("admin:accounts_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
    
    def test_user_add_works(self):
        """Test user add page works"""
        url = reverse("admin:accounts_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    

