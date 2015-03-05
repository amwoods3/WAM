from django.db import models

# Create your models here.

class UserLogin(models.Model):
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

# only for active games
class Game(models.Model):
    game_name = models.CharField(max_length=100)
    game_state = models.CharField(max_length=200)
    last_move = models.CharField(max_length=80)
    game_history = models.CharField(max_length=200)
    player1_id = models.PositiveIntegerField()
    player2_id = models.PositiveIntegerField()
    timer = models.PositiveIntegerField()
    is_player1_turn = models.BooleanField(default=True)
    player1_ai = models.FilePathField(path="/scripts", match="*.py", recursive=True)
    player2_ai = models.FilePathField(path="/scripts", match="*.py", recursive=True)


class UserAiTable(models.Model):
    user_id = models.PositiveIntegerField()
    user_ai_gen_title = models.FilePathField(path="/scripts", match="*.py", recursive=True)
    user_ai_title = models.CharField(max_length=100)
