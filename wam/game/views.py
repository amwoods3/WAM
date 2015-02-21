from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf

from forms import *#UploadFileForm

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
    return HttpResponse("The two ai's were successfully upload")

def play(request):
    import sys
    sys.path.insert(0, 'ais')
    sys.path.insert(0, '../tictactoe/')
    import tictactoe
    from html_change import *
    s = tictactoe.play_game(ai=['ai1', 'randai'])
    return HttpResponse(change(s))
