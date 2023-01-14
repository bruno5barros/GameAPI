from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from common.date_utils import convert_str_date
from common.tests.utils import create_user


BIRTHDATE = convert_str_date("1987-09-10")


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.admin_user = create_user(
            get_user_model().objects.create_superuser,
            email="nuno@b.com",
            password="12345",
            username="nuno",
            birthdate=BIRTHDATE,
        )

        self.user = create_user(
            get_user_model().objects.create_user,
            email="b@b.com",
            password="12345",
            username="barros",
            birthdate=BIRTHDATE,
        )

        self.client.force_login(self.admin_user)

    def test_users_listed(self):
        """Test that users are listed on user page"""
        url = reverse("admin:user_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.username)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test the user edit page works"""
        url = reverse("admin:user_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that create user page works"""
        url = reverse("admin:user_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
