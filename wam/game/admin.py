from django.contrib import admin

from game.models import ActiveGame, UserLogin, UserAiTable, PastGames, UserStats

# Register your models here.
admin.site.register(ActiveGame)
admin.site.register(UserLogin)
admin.site.register(UserAiTable)
admin.site.register(PastGames)
admin.site.register(UserStats)
