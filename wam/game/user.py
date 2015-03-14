from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf

from game.models import UserAiTable, UserStats, UserLogin
from game.views import logged_in

def view_user_profile(request):
    c = {'user_logged_in': logged_in(request)}
    if logged_in(request):
        loggin_user_name = UserLogin.objects.get(pk=request.session['member_id']).user_name
        c['user_name'] = loggin_user_name
    else:
        return HttpResponseRedirect('/game')

    scores = UserStats.objects.all().filter(user_id=request.session['member_id'])
    c['score_list'] = scores

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