from django.shortcuts import render
from django.http import HttpResponseRedirect

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
    
    
