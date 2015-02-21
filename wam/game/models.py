from django.db import models

# Create your models here.
class Game(models.Model):
    game_name = models.CharField(max_length=100)
    game_state = models.CharField(max_length=200)
    last_move = models.CharField(max_length=80)
    player1_name = models.CharField(max_length=50)
    player2_name = models.CharField(max_length=50)
    timer = models.PositiveIntegerField()
    is_player1_turn = models.BooleanField(default=True)
    player1_ai = models.FilePathField(path="/scripts", match="*.py", recursive=True)
    player2_ai = models.FilePathField(path="/scripts", match="*.py", recursive=True)
