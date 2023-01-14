import tempfile
import os
from datetime import date
from PIL import Image
from common.date_utils import convert_str_date, convert_date_str
from common.tests.utils import create_user
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


USERS_URL = reverse("user:user-list")
TOKEN_URL = reverse("user:token")
BIRTHDATE = convert_str_date("1987-09-10")


def image_url(user_id):
    """Return url for the user image"""
    return reverse("user:user-detail", args=[user_id])


PAYLOAD = {
    "email": "bb@b.com",
    "password": "12345",
    "username": "b",
    "birthdate": BIRTHDATE,
}

PAYLOAD_LOGIN = {"email": "bb@b.com", "password": "12345"}


class PublicUserAPITests(TestCase):
    """Test the users public API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_sucess(self):
        """Creating a user with a valid payload"""
        res = self.client.post(USERS_URL, PAYLOAD)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        del res.data["image"]

        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(PAYLOAD.get("password", None)))
        self.assertNotIn("password", res.data)

    def test_user_exists(self):
        """Test creating user that already exists fails"""
        self.client.post(USERS_URL, PAYLOAD)

        res = self.client.post(USERS_URL, PAYLOAD)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password must be more than 5 characters"""
        payload = PAYLOAD.copy()
        payload["password"] = "1234"
        res = self.client.post(USERS_URL, payload)
        is_user_exists = (
            get_user_model().objects.filter(
                email=payload.get("email", None)).exists()
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(is_user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for user"""
        res = self.client.post(USERS_URL, PAYLOAD)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.post(TOKEN_URL, PAYLOAD_LOGIN)

        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credential(self):
        """Test that token is not created if invalid credentials are given"""
        res = self.client.post(USERS_URL, PAYLOAD)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        PAYLOAD_LOGIN["password"] = "12346"
        res = self.client.post(TOKEN_URL, PAYLOAD_LOGIN)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user does not exists"""
        res = self.client.post(
            TOKEN_URL,
            {"email": PAYLOAD.get("email"),
             "password": PAYLOAD.get("password")},
        )

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(
            TOKEN_URL,
            {
                "email": "b",
                "password": "",
            },
        )

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_new_user_invalid_password(self):
        """Test creating user without password raises error"""
        payload = PAYLOAD.copy()
        payload["password"] = ""
        res = self.client.post(USERS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", res.data)

    def test_new_user_invalid_username(self):
        """Test creating user without email raises error"""
        payload = PAYLOAD.copy()
        payload["email"] = ""
        res = self.client.post(USERS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", res.data)

    def test_new_user_invalid_birthdate(self):
        """Test creating user without birthdate raises error"""
        payload = PAYLOAD.copy()
        payload["birthdate"] = ""

        res = self.client.post(USERS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("birthdate", res.data)

    def test_new_user_under_18(self):
        """Test creating user under 18 years old"""
        payload = PAYLOAD.copy()
        birthdate = convert_str_date(convert_date_str(date.today()))
        payload["birthdate"] = birthdate

        res = self.client.post(USERS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("birthdate", res.data)

    def test_get_list_users_played_games(self):
        """Request all users and last played game with an anonymous user"""
        res = self.client.get(USERS_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_list_of_users(self):
        """Request all users with an anonymous user"""
        res = self.client.get(USERS_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateUserAPITests(TestCase):
    """Test the users private API"""

    def setUp(self):
        self.client = APIClient()

        self.super_user = create_user(
            get_user_model().objects.create_superuser,
            email="b@b.com",
            password="12345",
            username="b",
            birthdate=convert_str_date("1987-09-10"),
        )
        self.user = create_user(
            get_user_model().objects.create_user,
            email="nuno@b.com",
            password="12345",
            username="nuno",
            birthdate=BIRTHDATE,
        )

    def test_get_list_of_users_staff(self):
        """Get all users with an authenticated staff user"""
        self.client.force_authenticate(user=self.super_user)
        res = self.client.get(USERS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), len(get_user_model().objects.all()))

    def test_get_list_of_users_authenticated(self):
        """Request all users with an authenticated user"""
        self.client.force_authenticate(user=self.user)
        res = self.client.get(USERS_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_list_users_played_games(self):
        """Get all users and last played game with a staff user"""
        self.client.force_authenticate(user=self.super_user)
        res = self.client.get(USERS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), len(get_user_model().objects.all()))

    def test_get_list_users_played_games_authenticated(self):
        """Request all users and last plyed game with an authenticated user"""
        self.client.force_authenticate(user=self.user)
        res = self.client.get(USERS_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class UserImageUploadTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.super_user = create_user(
            get_user_model().objects.create_superuser,
            email="b@b.com",
            password="12345",
            username="b",
            birthdate=convert_str_date("1987-09-10"),
        )
        self.client.force_authenticate(user=self.super_user)

    def tearDown(self):
        self.super_user.image.delete()

    def upload_image_bad_request(self):
        """Test uploading an invalid image"""
        url = image_url(self.super_user.id)
        res = self.client.post(url, {"image": "notimage"}, format="multipart")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_image_user(self):
        """Test uploading an user image"""
        payload = PAYLOAD.copy()
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            payload["image"] = ntf

            res = self.client.post(USERS_URL, payload, format="multipart")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn("image", res.data)

    def test_update_upload_image_user(self):
        """Test uploading an user image"""
        payload = PAYLOAD.copy()
        url = image_url(self.super_user.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            payload["image"] = ntf
            payload["email"] = self.super_user.email

            res = self.client.put(url, payload, format="multipart")
        self.super_user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("image", res.data)
        self.assertEqual(res.data["email"], self.super_user.email)
        self.assertTrue(os.path.exists(self.super_user.image.path))
