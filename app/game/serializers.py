from rest_framework import serializers
from game.models import Game, PlaySession, Genre
from user.serializers import UserSerializer


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for genre object"""

    class Meta:
        model = Genre
        fields = ('id', 'name')


class GameSerializer(serializers.ModelSerializer):
    """Serializer for game object"""
    genre = GenreSerializer(many=True)

    class Meta:
        model = Game
        fields = ('name', 'genre')
        depth = 1


class PlaySessionSerializerStore(serializers.ModelSerializer):
    """Serializer for play session object"""

    class Meta:
        model = PlaySession
        fields = ('user', 'game', 'creation_time')
        read_only_fields = ('user', )

    def create(self, validated_data, **kwargs):
        validated_data['user'] = self.context.get('request').user
        return PlaySession.objects.create(**validated_data)


class PlaySessionSerializer(serializers.ModelSerializer):
    """Serializer for play session object"""
    user = UserSerializer()
    game = GameSerializer()

    class Meta:
        model = PlaySession
        fields = ('user', 'game', 'creation_time')
        read_only_fields = ('user', )
        depth = 2
