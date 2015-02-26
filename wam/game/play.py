from django.shortcuts import render
from django.http import HttpResponse
from game.models import UserLogin

def challenge_users_ai(request):
    users = UserLogin.objects.all().values_list('user_name')
    can_challenge = {'can_challenge': users}
    return render(request, 'game/challenge_users_ai.html', can_challenge)

def view_user(request):
    pass
def play(request):
    import sys
    sys.path.insert(0, 'ais')
    sys.path.insert(0, '../tictactoe/')
    import tictactoe
    from html_change import *
    s = tictactoe.play_game(ai=['ai1', 'randai'])
    return HttpResponse(change(s))
