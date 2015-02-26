from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf
from django.http import Http404

from forms import UploadFileForm, UserRegisterForm, UserLoginForm
from game.models import UserLogin

def handle_uploaded_file(f, n):
    with open('ais/' + n + '.py', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

# Create your views here.
def index(request):
    return render(request, 'game/index.html')

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            post = request.POST
            files = request.FILES
            handle_uploaded_file(files['player1_ai_code'],
                                 post['player1_ai_title'])
            handle_uploaded_file(files['player2_ai_code'],
                                 post['player2_ai_title'])
            return HttpResponseRedirect('/game/challenge_user')
    else:
        form = UploadFileForm()
    c = {'form': form}
    c.update(csrf(request))
    return render_to_response('game/upload.html', c)

def play(request):
    import glob
    import sys
    sys.path.insert(0, 'ais')
    sys.path.insert(0, '../tictactoe/')
    import tictactoe
    from html_change import *
    s = tictactoe.play_game(ai=['ai1', 'randai'])
    return HttpResponse(change(s))

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            post = request.POST
            # check if the user exists in the database
            check_user_exists = UserLogin.objects.filter(user_name=post['user_name'])
            if check_user_exists:
                c = {'form': form,
                     'error_message': "This user name already exists."}
                c.update(csrf(request))
                return render_to_response('game/register.html', c)
            # check size of user name
            if len(post['user_name']) < 5:
                c = {'form': form,
                     'error_message': "Your username must be longer than 5 characters."}
                c.update(csrf(request))
                return render_to_response('game/register.html', c)
            # check size of password
            if len(post['password']) < 5:
                c = {'form': form,
                     'error_message': "Your password must be longer than 5 characters."}
                c.update(csrf(request))
                return render_to_response('game/register.html', c)
            # check if passwords match -- for the form
            if post['password'] != post['re_password']:
                c = {'form': form,
                     'error_message': "Your passwords do not match"}
                c.update(csrf(request))
                return render_to_response('game/register.html', c)
            # registeration successful
            user = UserLogin(user_name=post['user_name'], password=post['password'])
            user.save()
            return HttpResponseRedirect('/game/login')
    else:
        form = UserRegisterForm()
    c = {'form': form}
    c.update(csrf(request))
    return render_to_response('game/register.html', c)
    
def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            m = UserLogin.objects.get(user_name=request.POST['user_name'])
            if m.password == request.POST['password']:
                request.session['member_id'] = m.id
                return  HttpResponseRedirect('/game')
            else:
                c = {'form': form,
                     'error_message': "Your username and password didn't match."}
                c.update(csrf(request))
                return render_to_respons('game/login.html', c)
    else:
        form = UserLoginForm()
    c = {'form': form}
    c.update(csrf(request))
    return render_to_response('game/login.html', c)

def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return HttpResponseRedirect("/game")
