from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from game.models import UserLogin
from django.core.context_processors import csrf

from game.views import logged_in
from game.models import UserLogin, UserAiTable

def challenge_users_ai(request):
    c = {'user_logged_in': logged_in(request)}
    if request.method == 'POST':
        user_id = UserLogin.objects.get(user_name=request.POST['ch_user'])
        request.session['challenged_user'] = user_id.id
        return HttpResponseRedirect('/game/view_user')
    
    users = UserLogin.objects.all().values_list('user_name')
    users = [x[0] for x in users]
    c['can_challenge'] = users
    c.update(csrf(request))
    return render_to_response('game/challenge_users_ai.html', c)

def view_user_ai(request):
    c = {'user_logged_in': logged_in(request)}
    if request.method == 'POST':
        request.session['ch_user_ai'] = request.POST['ch_ai']
        request.session['user_ai'] = request.POST['my_ai']
        return HttpResponseRedirect('/game/play')

    # collect challenged users AI list
    ais = UserAiTable.objects.all().filter(user_id=request.session['challenged_user'])
    ais = [x.user_ai for x in ais]
    c['ai_list'] = ais

    # collect user logged in AI list
    ais = UserAiTable.objects.all().filter(user_id=request.session['member_id'])
    ais = [x.user_ai for x in ais]
    c['ai_list2'] = ais

    # collect challenged users user_name
    user = UserLogin.objects.get(pk=request.session['challenged_user'])
    c['user_name'] = user.user_name
    c.update(csrf(request))
    return render_to_response('game/view_user.html', c)

def play(request):
    challenged_user_name = UserLogin.objects.get(pk=request.session['challenged_user']).user_name
    loggin_user_name = UserLogin.objects.get(pk=request.session['member_id']).user_name
    import sys
    sys.path.insert(0, 'wam/ais/'+challenged_user_name+'/')
    sys.path.insert(0, 'wam/ais/'+loggin_user_name+'/')
    sys.path.insert(0, 'tictactoe/')
    import tictactoe
    from html_change import change
    s = tictactoe.play_game(ai=[request.session['user_ai'], request.session['ch_user_ai']])
    return HttpResponse(change(s))
