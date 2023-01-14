from game.models import Game, Genre
from common.date_utils import convert_date_str


def create_user(create_user, **params):
    return create_user(**params)


def create_genres():
    """Create new three genres"""
    genres = ["Shooter", "Shooter", "Third Person Shooter"]
    return [Genre.objects.create(name=genre) for genre in genres]


def create_game(name="Game1"):
    return Game.objects.create(name=name)


def create_expected_data(game_db: Game) -> dict:
    """Create the expected game data dict"""
    expected_game = {}
    expected_game["name"] = game_db.name
    expected_game["genre"] = [
        {"id": genre.id, "name": genre.name} for genre in game_db.genre.all()
    ]
    return expected_game


def create_expected_data_user(user_db) -> dict:
    """Create the expected user data dict"""
    if user_db:
        return {
            "id": user_db.id,
            "email": user_db.email,
            "username": user_db.username,
            "birthdate": convert_date_str(user_db.birthdate),
            "image": None,
        }


def create_expected_data_list(play_session, user, *created_data):
    """Build the expected data list"""
    if created_data:
        expected_data_list = []
        for i, data in enumerate(created_data):
            expected_data = create_expected_data(data)
            if play_session:
                expected_data_tmp = {}
                expected_data_tmp["user"] = create_expected_data_user(user)
                expected_data_tmp["game"] = expected_data
                expected_data_tmp["creation_time"] = play_session[i][
                    "creation_time"]
                expected_data = expected_data_tmp
            expected_data_list.append(expected_data)
        return expected_data_list
