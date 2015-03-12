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

    ais = UserAiTable.objects.all().filter(user_id=request.session['member_id'])
    ais = [x.user_ai_title for x in ais]
    c['ai_list'] = ais

    return render(request, 'game/view_user_profile.html', c)
    
    
