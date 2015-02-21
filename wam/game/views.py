from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf
from django.http import Http404

from forms import UploadFileForm, RegisterUser

def handle_uploaded_file(f, n):
    with open('ais/' + n + '.py', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the game index.")

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
            return HttpResponseRedirect('/game/successful_upload')
    else:
        form = UploadFileForm()
    c = {'form': form}
    c.update(csrf(request))
    return render_to_response('game/upload.html', c)

def successful_upload(request):
    return HttpResponse("The two ai's were successfully upload.")

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
        form = RegisterUser(request.POST)
        if form.is_valid():
            from game.models import UserLogin
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
            return HttpResponseRedirect('/game/successful_registeration')
    else:
        form = RegisterUser()
    c = {'form': form}
    c.update(csrf(request))
    return render_to_response('game/register.html', c)

def successful_registeration(request):
    return HttpResponse("Your registration was successful.")
    
