from game.models import PlaySession
from common.date_utils import convert_str_date
from common.tests.utils import (
    create_user,
    create_game,
    create_genres,
    create_expected_data_list,
)
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


PLAY_SESSION_URL = reverse("game:playsession-list")
BIRTHDATE = convert_str_date("1987-09-10")


def detail_url(play_session_id):
    """Return playsession detail url"""
    return reverse("game:playsession-detail", args=[play_session_id])


def get_play_session(id):
    """Retreive a play session based on id"""
    return PlaySession.objects.get(pk=id)


def create_play_session(user, game):
    """Retreive a play session based on id"""
    return PlaySession.objects.create(user=user, game=game)


class PublicPlaySession(TestCase):
    """Test the play session public api"""

    def setUp(self):
        self.client = APIClient()
        genres = create_genres()
        self.game = create_game()
        self.game.genre.set(genres)
        self.payload = {"game": self.game}

    def test_create_play_session(self):
        """Try to create a play session as anonymous"""
        res = self.client.post(PLAY_SESSION_URL, self.payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_play_session(self):
        """List play session as anonymous"""
        res = self.client.get(PLAY_SESSION_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_play_session(self):
        """Get play session as anonymous"""
        res = self.client.get(detail_url(1))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_play_session(self):
        """Update play session as anonymous"""
        res = self.client.put(detail_url(1), self.payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_play_session(self):
        """Delete a play session as anonymous"""
        res = self.client.delete(detail_url(1), self.payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivatePlaySession(TestCase):
    """Test the play session private api"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            get_user_model().objects.create_user,
            email="nuno@b.com",
            password="12345",
            username="nuno",
            birthdate=BIRTHDATE,
        )
        self.super_user = create_user(
            get_user_model().objects.create_superuser,
            email="b@b.com",
            password="12345",
            username="b",
            birthdate=convert_str_date("1987-09-10"),
        )
        genres = create_genres()
        self.game = create_game()
        self.game.genre.set(genres)
        self.payload = {"game": self.game.id}

    def test_create_play_session_user(self):
        """Try to create a play session as authenticated user"""
        self.client.force_authenticate(user=self.user)
        res = self.client.post(PLAY_SESSION_URL, self.payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        play_sesseion = PlaySession.objects.all()
        self.assertEqual(len(play_sesseion), 1)

    def test_list_play_session_user(self):
        """List play session as authenticated user"""
        self.client.force_authenticate(user=self.user)
        create_play_session(self.user, self.game)

        res = self.client.get(PLAY_SESSION_URL)
        expected_data = create_expected_data_list(
            res.data, self.user, self.game)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, expected_data)

    def test_detail_play_session_user(self):
        """Get play session as authenticated user"""
        self.client.force_authenticate(user=self.user)
        play_session = create_play_session(self.user, self.game)

        res = self.client.get(detail_url(play_session.id))
        expected_data = create_expected_data_list(
            [res.data], self.user, self.game)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, expected_data[0])

    def test_update_play_session_user(self):
        """Update play session as authenticated user"""
        self.client.force_authenticate(user=self.user)
        play_session = create_play_session(self.user, self.game)
        payload = self.payload.copy()
        payload["creation_time"] = "2023-01-10T16:57:48.401961Z"

        res = self.client.put(detail_url(play_session.id), payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(res.data.get("creation_time"),
                            payload["creation_time"])

    def test_delete_play_session_user(self):
        """Delete a play session as authenticated user"""
        self.client.force_authenticate(user=self.user)
        play_session = create_play_session(self.user, self.game)

        res = self.client.delete(detail_url(play_session.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(PlaySession.objects.all()), 0)

    def test_create_play_session_super_user(self):
        """Try to create a play session as authenticated superuser"""
        self.client.force_authenticate(user=self.super_user)
        res = self.client.post(PLAY_SESSION_URL, self.payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        play_sesseion = PlaySession.objects.all()
        self.assertEqual(len(play_sesseion), 1)

    def test_list_play_session_super_user(self):
        """List play session as authenticated super user"""
        self.client.force_authenticate(user=self.super_user)
        create_play_session(self.super_user, self.game)

        res = self.client.get(PLAY_SESSION_URL)
        expected_data = create_expected_data_list(
            res.data, self.super_user, self.game)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, expected_data)

    def test_detail_play_session_super_user(self):
        """Get play session as authenticated super user"""
        self.client.force_authenticate(user=self.super_user)
        play_session = create_play_session(self.super_user, self.game)

        res = self.client.get(detail_url(play_session.id))
        expected_data = create_expected_data_list(
            [res.data], self.super_user, self.game
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, expected_data[0])

    def test_update_play_session_super_user(self):
        """Update play session as authenticated super user"""
        self.client.force_authenticate(user=self.super_user)
        play_session = create_play_session(self.super_user, self.game)
        payload = self.payload.copy()
        payload["creation_time"] = "2023-01-10T16:57:48.401961Z"

        res = self.client.put(detail_url(play_session.id), payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(res.data.get("creation_time"),
                            payload["creation_time"])

    def test_delete_play_session_super_user(self):
        """Delete a play session as authenticated super user"""
        self.client.force_authenticate(user=self.super_user)
        play_session = create_play_session(self.super_user, self.game)

        res = self.client.delete(detail_url(play_session.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(PlaySession.objects.all()), 0)
