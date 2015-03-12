from django.shortcuts import render
from django.http import HttpResponseRedirect
from game.models import UserLogin
from django.core.context_processors import csrf

from game.views import logged_in
from game.models import UserLogin, UserAiTable, UserStats
from config import FILE_PATH

def challenge_users_ai(request):
    try:
        del request.session['played']
    except:
        pass
    
    c = {'user_logged_in': logged_in(request)}
    if logged_in(request):
        loggin_user_name = UserLogin.objects.get(pk=request.session['member_id']).user_name
        c['user_name'] = loggin_user_name
    else:
        return HttpResponseRedirect('/game')
    
    if request.method == 'POST':
        user_id = UserLogin.objects.get(user_name=request.POST['ch_user'])
        request.session['challenged_user'] = user_id.id
        return HttpResponseRedirect('/game/view_user')
    
    users = UserLogin.objects.all()
    users = [x.user_name for x in users if UserAiTable.objects.all().filter(user_id=x.id)]
    c['can_challenge'] = users
    c.update(csrf(request))
    return render(request, 'game/challenge_users_ai.html', c)

def view_user_ai(request):
    c = {'user_logged_in': logged_in(request)}
    if logged_in(request):
        loggin_user_name = UserLogin.objects.get(pk=request.session['member_id']).user_name
        c['user_name'] = loggin_user_name
    else:
        return HttpResponseRedirect('/game')
    
    if request.method == 'POST':
        # get the generated string for the uploaded ai
        user = UserAiTable.objects.get(user_ai_title=request.POST['my_ai'])
        ch = UserAiTable.objects.get(user_ai_title=request.POST['ch_ai'])
        request.session['ais'] = (user.user_ai_gen_title, ch.user_ai_gen_title)
        request.session['ai_title'] = (user.user_ai_title, ch.user_ai_title)
        return HttpResponseRedirect('/game/play')

    # collect challenged users AI list
    ais = UserAiTable.objects.all().filter(user_id=request.session['challenged_user'])
    ais = [x.user_ai_title for x in ais]
    c['ai_list'] = ais

    # collect user logged in AI list
    ais = UserAiTable.objects.all().filter(user_id=request.session['member_id'])
    ais = [x.user_ai_title for x in ais]
    c['ai_list2'] = ais

    # collect challenged users user_name
    user = UserLogin.objects.get(pk=request.session['challenged_user'])
    c['ch_user_name'] = user.user_name
    c.update(csrf(request))
    return render(request, 'game/view_user.html', c)

def play(request):
    c = {'user_logged_in': logged_in(request)}
    
    challenged_user_name = UserLogin.objects.get(pk=request.session['challenged_user']).user_name
    loggin_user_name = UserLogin.objects.get(pk=request.session['member_id']).user_name
    c['user_name'] = loggin_user_name
    c['ch_user_name'] = challenged_user_name
    c['user_name_ai'] = request.session['ai_title'][0]
    c['ch_name_ai'] = request.session['ai_title'][1]
     
    if not logged_in(request):
        return HttpResponseRedirect('/game')

    # the game is already played
    if request.session.get('played', False):
        c['game'] = request.session['played'][0]
        c['history'] = request.session['played'][1]
        c['winner'] = request.session['played'][2]
        return render(request, 'game/play.html', c)

    # import files to play the game
    import sys
    sys.path.insert(0, '%swam/ais/' % (FILE_PATH)+challenged_user_name+'/')
    sys.path.insert(0, '%swam/ais/' % (FILE_PATH)+loggin_user_name+'/')
    sys.path.insert(0, '%sgames/'  % (FILE_PATH))
    import tictactoe

    # play the game and create session to show that its already played
    s = tictactoe.play_game(ai=[request.session['ais'][1], request.session['ais'][0]])
    request.session['played'] = s
    c['game'] = s[0]
    c['history'] = s[1]
    c['winner'] = s[2]
    
    return render(request, 'game/play.html', c)
