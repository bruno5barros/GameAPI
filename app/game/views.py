from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from game.models import Game, PlaySession
from game.serializers import (
    GameSerializer,
    PlaySessionSerializer,
    PlaySessionSerializerStore,
)
from common.jwt_utils import JWTAuthentication


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    """This viewset automatically provides `list` and `retrieve` actions."""

    queryset = Game.objects.prefetch_related("genre").all()
    serializer_class = GameSerializer


class PlaySessionViewSet(viewsets.ModelViewSet):
    """This viewset automatically provides all actions."""

    queryset = PlaySession.objects.prefetch_related(
        "game__genre").select_related("user", "game").all()
    serializer_class = PlaySessionSerializerStore
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == "list" or self.action == "retrieve":
            self.serializer_class = PlaySessionSerializer
        return self.serializer_class
