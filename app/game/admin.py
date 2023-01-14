from django.contrib import admin
from game.models import Game, PlaySession, Genre


class GameAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    ordering = ['id']


class GenreAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    ordering = ['id']


class PlaySessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'creation_time']
    ordering = ['id']


admin.site.register(PlaySession, PlaySessionAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Game, GameAdmin)
