from django.urls import path, include
from rest_framework.routers import DefaultRouter
from game.views import GameViewSet, PlaySessionViewSet


router = DefaultRouter()
router.register("playsessions", PlaySessionViewSet)
router.register("games", GameViewSet)


app_name = "game"

urlpatterns = [
    path('', include(router.urls)),
]
