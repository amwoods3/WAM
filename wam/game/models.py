from django.db import models

# Create your models here.

class UserLogin(models.Model):
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

class UserAiTable(models.Model):
    user_id = models.PositiveIntegerField()
    user_ai_gen_title = models.FilePathField(path="/scripts", match="*.py", recursive=True)
    user_ai_title = models.CharField(max_length=100)
    user_ai_game_name = models.CharField(max_length=50)

class ActiveGame(models.Model):
    game_state = models.CharField(max_length=800)
    last_move = models.CharField(max_length=80)
    player1_id = models.PositiveIntegerField()
    player2_id = models.PositiveIntegerField()
    player1_timer = models.PositiveIntegerField(default=0)
    player2_timer = models.PositiveIntegerField(default=0)
    is_player1_turn = models.BooleanField(default=True)
    player1_ai = models.FilePathField(path="/scripts", match="*.py", recursive=True)
    player2_ai = models.FilePathField(path="/scripts", match="*.py", recursive=True)
    game_type = models.CharField(max_length=50, default='temp')

class PastGames(models.Model):
    player1_id = models.PositiveIntegerField()
    player2_id = models.PositiveIntegerField()
    game_history = models.CharField(max_length=300)
    did_player1_win = models.BooleanField(default=True)
    player1_ai_title = models.CharField(max_length=100)
    player2_ai_title = models.CharField(max_length=100)
    player1_total_time = models.PositiveIntegerField(default=0)
    player2_total_time = models.PositiveIntegerField(default=0)
    game_type = models.CharField(max_length=50, default='temp')


class UserStats(models.Model):
    user_id = models.PositiveIntegerField()
    user_ai_title = models.CharField(max_length=100)
    user_ai_wins = models.PositiveIntegerField()
    user_ai_losses = models.PositiveIntegerField()
    user_ai_draws = models.PositiveIntegerField()
    game_type = models.CharField(max_length=50, default='temp')
