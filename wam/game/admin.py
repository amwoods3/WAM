from django.contrib import admin

from game.models import ActiveGame, UserLogin, UserAiTable

# Register your models here.
admin.site.register(ActiveGame)
admin.site.register(UserLogin)
admin.site.register(UserAiTable)
