from common.date_utils import convert_str_date
from common.tests.utils import (
    create_user,
    create_game,
    create_genres,
    create_expected_data,
    create_expected_data_list,
)
from game.models import Genre
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status


GAME_LIST_URL = reverse("game:game-list")
BIRTHDATE = convert_str_date("1987-09-10")


def game_detail_url(game_id):
    """Return game detail url"""
    return reverse("game:game-detail", args=[game_id])


def create_genre(name="teste1"):
    return Genre.objects.create(name=name)


def create_games():
    game1 = create_game()
    game1.genre.set(create_genres())
    game2 = create_game("Game2")
    game2.genre.add(create_genre())

    return game1, game2


class PublicGameAPITests(TestCase):
    """Test the game public API"""

    def setUp(self):
        self.client = APIClient()

    def test_get_list_of_games(self):
        """Retrieve the list of al games"""
        game1, game2 = create_games()

        res = self.client.get(GAME_LIST_URL)
        expected_data = create_expected_data_list(False, None, game1, game2)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, expected_data)

    def test_get_detail_of_games(self):
        """Retrieve the datail of selected game"""
        game1, game2 = create_games()

        detail_url = game_detail_url(game2.id)
        res = self.client.get(detail_url)
        expected_data = create_expected_data(game2)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, expected_data)


class PrivateGameAPITests(TestCase):
    """Test the game private API"""

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
            username="barros",
            birthdate=BIRTHDATE,
        )

    def test_get_list_of_games_user(self):
        """Retrieve the list of al games with authenticated user"""
        game1, game2 = create_games()

        self.client.force_authenticate(user=self.user)
        res = self.client.get(GAME_LIST_URL)
        expected_data = create_expected_data_list(False, None, game1, game2)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, expected_data)

    def test_get_detail_of_games_user(self):
        """Retrieve the datail of selected game with authenticated user"""
        game1, game2 = create_games()

        self.client.force_authenticate(user=self.user)
        detail_url = game_detail_url(game2.id)
        res = self.client.get(detail_url)
        expected_data = create_expected_data(game2)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, expected_data)

    def test_get_list_of_games_suser(self):
        """Retrieve the list of all games with authenticated super user"""
        game1, game2 = create_games()

        self.client.force_authenticate(user=self.super_user)
        res = self.client.get(GAME_LIST_URL)
        expected_data = create_expected_data_list(False, None, game1, game2)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, expected_data)

    def test_get_detail_of_games_suser(self):
        """Retrieve the game datail with authenticated super user"""
        game1, game2 = create_games()

        self.client.force_authenticate(user=self.super_user)
        detail_url = game_detail_url(game2.id)
        res = self.client.get(detail_url)
        expected_data = create_expected_data(game2)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, expected_data)
