from django.contrib import admin

from game.models import Game, UserLogin, UserAiTable

# Register your models here.
admin.site.register(Game)
admin.site.register(UserLogin)
admin.site.register(UserAiTable)
