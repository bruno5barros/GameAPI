from django.db import models
from app.settings import AUTH_USER_MODEL


class Genre(models.Model):
    """Genre model"""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Game(models.Model):
    """Game model"""
    name = models.CharField(max_length=255)
    genre = models.ManyToManyField(Genre)

    def __str__(self):
        return self.name


class PlaySession(models.Model):
    """Play session model"""
    user = models.ForeignKey(AUTH_USER_MODEL,
                             related_name='last_played_session',
                             on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    creation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.game}({self.creation_time})"
