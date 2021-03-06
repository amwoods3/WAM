from django.shortcuts import render
from django.http import HttpResponseRedirect
from game.models import UserLogin
from django.core.context_processors import csrf

from game.views import logged_in
from game.models import UserLogin, UserAiTable, UserStats, PastGames
from config import FILE_PATH

def challenge_user(request):
    try:
        del request.session['played']
        del request.session['game_type']
    except:
        pass
    
    c = {'user_logged_in': logged_in(request)}
    if logged_in(request):
        loggin_user_name = UserLogin.objects.get(pk=request.session['member_id']).user_name
        c['user_name'] = loggin_user_name
    else:
        return HttpResponseRedirect('/game')
    
    if request.method == 'POST':
        # get the challenged user's username
        user_id = UserLogin.objects.get(user_name=request.POST['ch_user'])
        request.session['challenged_user'] = user_id.id

        # get the game type
        if request.POST['game'] == 'tic_tac_toe':
            request.session['game_type'] = 'tic_tac_toe'
        elif request.POST['game'] == 'checkers':
            request.session['game_type'] = 'checkers'

        # Ai V Ai
        if request.POST['game_type'] == 'AivAi':
            return HttpResponseRedirect('/game/view_user_ai')
        else:
            c['error_message'] = 'Sorry the game mode %s is not available yet.' % request.POST['game_type']
    
    users = UserLogin.objects.all()
    users = [x.user_name for x in users if UserAiTable.objects.all().filter(user_id=x.id)]
    c['can_challenge'] = users
    c.update(csrf(request)) 
    return render(request, 'game/challenge_user.html', c)

def view_user_ai(request):
    c = {'user_logged_in': logged_in(request)}
    if logged_in(request):
        loggin_user_name = UserLogin.objects.get(pk=request.session['member_id']).user_name
        c['user_name'] = loggin_user_name
    else:
        return HttpResponseRedirect('/game')
    
    if request.method == 'POST':
        # get the generated string for the uploaded ai
        user = UserAiTable.objects.get(user_id = request.session['member_id'],
                                       user_ai_title=request.POST['my_ai'])
        ch = UserAiTable.objects.get(user_id = request.session['challenged_user'],
                                     user_ai_title=request.POST['ch_ai'])
        request.session['ais'] = (user.user_ai_gen_title, ch.user_ai_gen_title)
        request.session['ai_title'] = (user.user_ai_title, ch.user_ai_title)

        if (request.session['member_id'] == request.session['challenged_user'] and
            request.POST['my_ai'] == request.POST['ch_ai']):
            request.session['same_file'] = 1

        try:
            if request.POST['game_time'] is not u"" or None:
                game_time = int(request.POST['game_time'])
            else:
                game_time = 0

            request.session['game_timer'] = game_time
            return HttpResponseRedirect('/game/play')
        except:
            c['error_message'] = 'Game timer must be an integer'

    # collect challenged users AI list
    ais = UserAiTable.objects.all().filter(user_id=request.session['challenged_user'],
                                          user_ai_game_name = request.session['game_type'])
    ais = [x.user_ai_title for x in ais]
    c['ai_list'] = ais

    # collect user logged in AI list
    ais = UserAiTable.objects.all().filter(user_id=request.session['member_id'],
                                           user_ai_game_name = request.session['game_type'])
    ais = [x.user_ai_title for x in ais]
    c['ai_list2'] = ais

    # collect challenged users user_name
    user = UserLogin.objects.get(pk=request.session['challenged_user'])
    c['ch_user_name'] = user.user_name
    c.update(csrf(request))
    return render(request, 'game/view_user_ai.html', c)

def unicode_to_str(to_change):
    new_list = []
    import unicodedata
    for item in to_change:
        sub_list = []
        for a in item:
            sub_list.append(unicodedata.normalize('NFKD', a).encode('ascii','ignore'))
        new_list.append(sub_list)
    return new_list

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

    c['game_type'] = request.session['game_type']
    c['p1'], c['p2'] = ('-', '-')
    if c['game_type'] == 'tic_tac_toe':
        c['p}1'], c['p2'] = ('x', 'o')
    elif c['game_type'] == 'checkers':
        c['p1'], c['p2'] = ('b', 'r')


    # the game is already played
    if request.session.get('played', False):
        c['game'] = request.session['played'][0]
        c['history'] = request.session['played'][1]
        c['winner'] = request.session['played'][2] if request.session['played'][2] != '!' else 'Draw'
        c['time1'] = request.session['played'][3]
        c['time2'] = request.session['played'][4]

        if isinstance(c['game'][0][0], unicode):
            c['game'] = unicode_to_str(c['game'])

        return render(request, 'game/play.html', c)

    # import files to play the game
    game_time = request.session['game_timer']
    import sys
    sys.path.insert(0, '%swam/ais/' % (FILE_PATH)+challenged_user_name+'/')
    sys.path.insert(0, '%swam/ais/' % (FILE_PATH)+loggin_user_name+'/')
    sys.path.insert(0, '%sgames/'  % (FILE_PATH))
    import game_runner

    # play the game and create session to show that its already played
    s = game_runner.play_game(users=[loggin_user_name, 
                                     challenged_user_name],
                              ais=[request.session['ais'][0], 
                                   request.session['ais'][1]], 
                              time=game_time,
                              game_type=request.session['game_type'])
    request.session['played'] = s
    c['game'] = s[0]
    c['history'] = s[1]
    c['winner'] = s[2] if s[2] != '!' else 'Draw'
    c['time1'] = s[3]
    c['time2'] = s[4]

    if isinstance(c['game'][0][0], unicode):
        c['game'] = unicode_to_str(c['game'])

    # find out who won
    is_draw = (c['winner'] == '!')
    user_won = (c['winner'] == 'x')

    # update stat table for user and challenged user
    user_stats = UserStats.objects.get(user_id=request.session['member_id'],
                                           user_ai_title=c['user_name_ai'])
    if 'same_file' in request.session:
        user_stats.user_ai_wins += 1
        user_stats.user_ai_losses += 1
        del request.session['same_file']
    else:
        ch_user_stats = UserStats.objects.get(user_id=request.session['challenged_user'],
                                              user_ai_title=c['ch_name_ai'])
        if user_won:
            user_stats.user_ai_wins += 1
            ch_user_stats.user_ai_losses += 1
        elif not is_draw:
            user_stats.user_ai_losses += 1
            ch_user_stats.user_ai_wins += 1
        else:
            user_stats.user_ai_draws += 1
            ch_user_stats.user_ai_draws += 1
        ch_user_stats.save()
    user_stats.game_type = request.session['game_type']
    user_stats.save()

    # add the game played to the past games table
    #  s[5] -> history for viewing game history on history page
    past_games = PastGames(player1_id = request.session['member_id'],
                           player2_id = UserLogin.objects.get(user_name=c['ch_user_name']).id,
                           player1_ai_title = c['user_name_ai'],
                           player2_ai_title = c['ch_name_ai'],
                           did_player1_win = user_won,
                           game_history = s[5],
                           player1_total_time = s[3],
                           player2_total_time = s[4],
                           game_type= request.session['game_type'])
    past_games.save()

    return render(request, 'game/play.html', c)