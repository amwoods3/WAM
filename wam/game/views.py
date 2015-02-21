from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf

from forms import UploadFileForm

def handle_uploaded_file(f):
    with open(f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the game index.")

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES
            for f in files:
                handle_uploaded_file(files[f])
            return HttpResponseRedirect('/game/successful_upload')
    else:
        form = UploadFileForm()
    c = {'form': form}
    c.update(csrf(request))
    return render_to_response('game/upload.html', c)

def successful_upload(request):
    return HttpResponse("stuff worked I guess")
