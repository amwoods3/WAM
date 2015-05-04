from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf

from game.models import UserAiTable, UserStats, UserLogin, PastGames, UserLogin
from game.views import logged_in

from config import FILE_PATH

def view_user_profile(request):
    c = {'user_logged_in': logged_in(request)}
    if logged_in(request):
        loggin_user_name = UserLogin.objects.get(pk=request.session['member_id']).user_name
        c['user_name'] = loggin_user_name
    else:
        return HttpResponseRedirect('/game')

    scores = UserStats.objects.all().filter(user_id=request.session['member_id'])
    c['score_list'] = scores

    games = PastGames.objects.all().filter(player1_id=request.session['member_id'])
    game_list = []
    for item in games:
    	opponent_name = UserLogin.objects.all().get(pk=item.player2_id).user_name
    	opponent_ai_title = item.player1_ai_title
    	win_loss = 'Win' if (item.did_player1_win == 1) else 'Lost'
    	your_time = item.player1_total_time
    	oppenent_time = item.player2_total_time
    	game_list.append((item.pk, opponent_name, opponent_ai_title, 
    					  win_loss, your_time, oppenent_time, item.game_type))

    games = PastGames.objects.all().filter(player2_id=request.session['member_id'])
    for item in games:
    	# check to see if element already exists
    	add = True
    	for a in game_list:
    		if item.pk in a:
    			add = False
    			break
    	if not add: continue

    	opponent_name = UserLogin.objects.all().get(pk=item.player1_id).user_name
    	opponent_ai_title = item.player2_ai_title
    	win_loss = 'Win' if (item.did_player1_win == 0) else 'Lost'
    	your_time = item.player2_total_time
    	oppenent_time = item.player1_total_time
    	game_list.append((item.pk, opponent_name, opponent_ai_title, 
    					  win_loss, your_time, oppenent_time, item.game_type))


    c['past_games'] = game_list

    return render(request, 'game/view_user_profile.html', c)

def forgot_password(request):
	c = {'user_logged_in': logged_in(request)}
	if logged_in(request):
		return HttpResponseRedirect('/game/logout')

	if request.method == 'POST':
	# check if the email entered exists in the databased
		check = UserLogin.objects.filter(email=request.POST['user_email'])
		if check:
			c['error_message'] = 'An email was sent to the account you have entered with the password'
			if len(check) > 1:
				c['error_message'] = 'Someone else is using your email.'
			else:
				user = UserLogin.objects.get(email=request.POST['user_email'])
			user_email = user.email
			user_name = user.user_name

			# check if the username entered match the the username in the database
			if request.POST['user_name'] != user_name:
				c['error_message'] = 'The username entered does not go with this email'
			else:
				from django.core.mail import send_mail
				send_mail('Password Recovery for project WAM', user.password,
						  'ciss438projectwam@google.com', [user_email], fail_silently=False)
		else:
			c['error_message'] = 'The email you have entered does not exist in the database.'

	return render(request, 'game/forgot_password.html', c)

def view_code(request):
	c = {'user_logged_in': logged_in(request)}
	if logged_in(request):
		loggin_user_name = UserLogin.objects.get(pk=request.session['member_id']).user_name
		c['user_name'] = loggin_user_name
	else:
		return HttpResponseRedirect('/game')

	# collect the code to view
	if request.method == 'POST':
		ai_title = request.POST['ai']
		code_obj = UserAiTable.objects.get(user_id=request.session['member_id'],
										   user_ai_title=ai_title)
		with open (FILE_PATH + 'wam/ais/' + c['user_name'] + '/' + code_obj.user_ai_gen_title + '.py', 
				   'r') as my_file:
			code = my_file.read()
		c['code'] = code 
		c['code_title'] = ai_title


	ais = UserAiTable.objects.all().filter(user_id=request.session['member_id'])
	ais = [x.user_ai_title for x in ais]
	c['ai_list'] = ais

	c.update(csrf(request))
	return render(request, 'game/view_code.html', c)

def view_game(request, game_id):
	c = {'user_logged_in': logged_in(request)}
	if logged_in(request):
		loggin_user_name = UserLogin.objects.get(pk=request.session['member_id']).user_name
		c['user_name'] = loggin_user_name
	else:
		return HttpResponseRedirect('/game')

	view_game = PastGames.objects.get(pk=game_id)
	import json
	import unicodedata
	game_history = unicodedata.normalize('NFKD', view_game.game_history).encode('ascii','ignore')

	view_history = json.loads(game_history)
	temp = '0) Initial Game State\n'
	num = 1
	for item in view_history:
		s = unicodedata.normalize('NFKD', item[0]).encode('ascii','ignore')
		temp += str(num) + ') ' + s + ': ' + str(item[1]) + '\n'
		num += 1	
	view_history = temp

	c['game_history'] = view_history
	c['game_id'] = game_id
	c['game_type'] = view_game.game_type
	c['p1'] = UserLogin.objects.get(pk=view_game.player1_id).user_name
	c['p2'] = UserLogin.objects.get(pk=view_game.player2_id).user_name
	c['p1_ai'] = view_game.player1_ai_title
	c['p2_ai'] = view_game.player2_ai_title
	c['p1_result'] = 'Win' if view_game.did_player1_win else 'Lost'
	c['p2_result'] = 'Lost' if view_game.did_player1_win else 'Win'

	if view_game.game_type == 'tic_tac_toe':
		c['p1_piece'] = 'x'
		c['p2_piece'] = 'y'
	elif view_game.game_type == 'checkers':
		c['p1_piece'] = 'b'
		c['p2_piece'] = 'r'

	if c['game_type'] == 'checkers':
		c['pieces'] = [[' ', 'b', ' ', 'b', ' ', 'b', ' ', 'b'], 
					   ['b', ' ', 'b', ' ', 'b', ' ', 'b', ' '], 
					   [' ', 'b', ' ', 'b', ' ', 'b', ' ', 'b'], 
					   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
					   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
					   ['r', ' ', 'r', ' ', 'r', ' ', 'r', ' '], 
					   [' ', 'r', ' ', 'r', ' ', 'r', ' ', 'r'], 
					   ['r', ' ', 'r', ' ', 'r', ' ', 'r', ' ']]
	elif c['game_type'] == 'tic_tac_toe':
		c['pieces'] = [[' ', ' ', ' '], 
		               [' ', ' ', ' '], 
                       [' ', ' ', ' ']]

	if request.method == 'POST':
		if request.POST.get('next'):
			request.session['game_index'] += 1
		elif request.POST.get('prev'):
			request.session['game_index'] -= 1
		elif request.POST.get('farnext'):
			request.session['game_index'] = len(request.session['list_of_states'])-1
		elif request.POST.get('farprev'):
			request.session['game_index'] = 0

		if request.session['game_index'] > len(request.session['list_of_states']) - 1:
			request.session['game_index'] = len(request.session['list_of_states']) - 1
			c['message'] = 'You are already at the last move in the game'
		if request.session['game_index'] < 0:
			c['message'] = 'You are already at the begining of the game'
			request.session['game_index'] = 0

		c['pieces'] = request.session['list_of_states'][request.session['game_index']]
		if isinstance(c['pieces'][0][0], unicode):
			new_list = []
			for item in c['pieces']:
				sub_list = []
				for a in item:
					sub_list.append(unicodedata.normalize('NFKD', a).encode('ascii','ignore'))
				new_list.append(sub_list)
		c['pieces'] = new_list
	else:
		request.session['game_index'] = 0
		import sys
		sys.path.insert(0, '%sgames/'  % (FILE_PATH))
		import historic_parser
		request.session['list_of_states'] = historic_parser.parse_history(game_history, 
																		  view_game.game_type)
		if not request.session['list_of_states']:
			request.session['list_of_states'] = c['pieces']

	c['game_index'] = request.session['game_index']

	c.update(csrf(request))
	return render(request, 'game/view_game.html', c)
