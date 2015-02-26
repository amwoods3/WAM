from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from game.models import UserLogin

from game.views import logged_in

def challenge_users_ai(request):
    c = {'user_logged_in': logged_in(request)}
    users = UserLogin.objects.all().values_list('user_name')
    users = [x[0] for x in users]
    c['can_challenge'] = users
    return render_to_response('game/challenge_users_ai.html', c)

def view_user(request):
    pass
def play(request):
    import sys
    sys.path.insert(0, 'ais')
    sys.path.insert(0, '../tictactoe/')
    import tictactoe
    from html_change import change
    s = tictactoe.play_game(ai=['ai1', 'randai'])
    return HttpResponse(change(s))
